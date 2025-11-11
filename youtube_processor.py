
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()


def extract_video_id_from_url(url):
    """Extract video ID from YouTube URL or return as-is if already an ID"""
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        parsed = urlparse(url)
        return parse_qs(parsed.query).get('v', [None])[0]
    else:
        return url  # Already a video ID


def get_transcript(video_id):
    """
    Extract transcript from YouTube video
    Returns: (success, transcript_text, metadata)
    """
    try:
        transcript_snippets = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        transcript_list = [s.text for s in transcript_snippets]
        transcript = " ".join(transcript_list)
        
        metadata = {
            'segments': len(transcript_snippets),
            'total_words': len(transcript.split()),
            'duration': transcript_snippets[-1].start if transcript_snippets else 0
        }
        
        return True, transcript, metadata
        
    except Exception as e:
        return False, str(e), {}


def create_chunks(transcript, chunk_size=800, chunk_overlap=100):
    """Split transcript into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.create_documents([transcript])
    return chunks


def create_vector_store(chunks):
    """Create FAISS vector store with embeddings"""
    # Use the same lightweight model - only 22MB!
    embeddings = HuggingFaceEmbeddings(
        model_name="paraphrase-MiniLM-L3-v2"
    )
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 10}
    )
    
    return vector_store, retriever


def format_docs(retrieved_docs):
    """Format retrieved documents into context text"""
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text


def create_rag_chain(retriever, model_name="gemini-2.5-flash-lite", temperature=0.2):
    """
    Create the complete RAG chain
    
    Available models:
    - "gemini-2.0-flash-exp" (RECOMMENDED - fastest, latest)
    - "gemini-1.5-pro" (more powerful)
    - "gemini-1.5-flash" (balanced)
    """
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature
    )
    
    # Create prompt template
    prompt = PromptTemplate(
        template="""
        You are a helpful assistant summarizing a YouTube video transcript.
        Use ONLY the given transcript context to answer questions, 
        but you can reasonably infer details if clearly implied in the text.

        Instructions:
        1. Give a well-structured, user-friendly answer.
        2. If unsure about something, clearly mention uncertainty.
        3. Avoid generic phrases like "insufficient context" — always explain what's missing.

        Context:
        {context}

        Question: {question}
        """,
        input_variables=['context', 'question']
    )
    
    # Create parallel chain
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })
    
    # Create output parser
    parser = StrOutputParser()
    
    # Create main chain
    main_chain = parallel_chain | prompt | llm | parser
    
    return main_chain


def process_video(video_id, chunk_size=800, chunk_overlap=100, model_name="gemini-2.5-flash-lite", temperature=0.2):
    """
    Complete function to process video and return RAG chain
    
    Returns: (success, main_chain, metadata, error_message)
    """
    try:
        # Step 1: Get transcript
        success, transcript, metadata = get_transcript(video_id)
        if not success:
            return False, None, {}, f"Failed to get transcript: {transcript}"
        
        # Step 2: Create chunks
        chunks = create_chunks(transcript, chunk_size, chunk_overlap)
        metadata['chunks'] = len(chunks)
        
        # Step 3: Create vector store
        vector_store, retriever = create_vector_store(chunks)
        
        # Step 4: Create RAG chain
        main_chain = create_rag_chain(retriever, model_name, temperature)
        
        return True, main_chain, metadata, None
        
    except Exception as e:
        return False, None, {}, str(e)


# ============================================================================
# EXAMPLE USAGE - Test your code
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🎥 Testing YouTube Video Processor")
    print("=" * 70)
    
    # Test with a video ID
    video_id = "Gfr50f6ZBvo"  # ← CHANGE THIS to test with your video
    
    print(f"\n📹 Processing video: {video_id}")
    print("-" * 70)
    
    # Process the video
    success, main_chain, metadata, error = process_video(video_id)
    
    if success:
        print(f"✅ Video processed successfully!")
        print(f"\n📊 Stats:")
        print(f"   - Segments: {metadata.get('segments', 0)}")
        print(f"   - Words: {metadata.get('total_words', 0):,}")
        print(f"   - Chunks: {metadata.get('chunks', 0)}")
        
        # Test some questions
        print("\n" + "=" * 70)
        print("💬 Testing Questions")
        print("=" * 70)
        
        questions = [
            "Can you summarize the video?",
            "What are the main topics discussed?",
            "Who is the speaker?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n🙋 Question {i}: {question}")
            print("-" * 70)
            answer = main_chain.invoke(question)
            print(f"🤖 Answer: {answer}\n")
    else:
        print(f"❌ Error: {error}")
        print("\n💡 Tips:")
        print("   - Check if video has captions enabled")
        print("   - Verify your GOOGLE_API_KEY in .env file")
        print("   - Make sure video ID is correct")
    
    print("\n" + "=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)