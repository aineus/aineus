`Presently in development. Expect working version in couple of days`

# AINeus

AINeus is an open-source news aggregation and transformation platform that allows users to consume news content through customizable AI prompts. What makes AINeus unique is its flexibility to work with different Language Models (LLMs) - from OpenAI's GPT to open-source models like Llama and Mistral.


## 🌟 Key Features

- **LLM Flexibility**: Switch between different AI models (OpenAI, Llama, Mistral) with simple configuration
- **Customizable News Prompts**: Create personal prompts to transform how news is presented
- **Daily News Digest**: Automated collection and processing of news from multiple sources
- **Efficient Caching**: Redis-based caching system for optimal performance
- **API-First Design**: Well-documented API endpoints for easy integration
- **Mobile-First UI**: Responsive design built with Next.js and Tailwind CSS

## 🚀 Tech Stack

### Backend
- FastAPI (Python 3.8+)
- PostgreSQL
- Redis
- Multiple LLM Support:
  - OpenAI GPT
  - Llama 2
  - Mistral
  - Extensible for other models
- SQLAlchemy
- Alembic

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- React Query

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Redis
- One of the following:
  - OpenAI API key
  - Local Llama 2 setup
  - Local Mistral setup

## 🛠️ Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/myneeos.git
cd myneeos
```

2. **Setup Backend**
```bash
cd backend
chmod +x setup_backend.sh
./setup_backend.sh
```

3. **Configure LLM**

Choose your preferred LLM by editing `.env`:

For OpenAI:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```

For Llama 2:
```env
LLM_PROVIDER=llama
LOCAL_LLM_URL=http://localhost:8001
LOCAL_LLM_MODEL=llama-2-7b
```

For Mistral:
```env
LLM_PROVIDER=mistral
LOCAL_LLM_URL=http://localhost:8001
LOCAL_LLM_MODEL=mistral-7b
```

4. **Start the Services**

Using Docker:
```bash
docker-compose up -d
```

Or manually:
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

5. **Access the Application**
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs


## 🔄 News Processing Flow

```mermaid
graph LR
    A[News Sources] --> B[Collector Service]
    B --> C[LLM Processing]
    C --> D[Cache Layer]
    D --> E[API Endpoints]
    E --> F[User Interface]
```

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports & Feature Requests

Please use the [issue tracker](https://github.com/my-neos/my-neos/issues) to report any bugs or file feature requests.

## ⭐ Support

If you like AINeus, please consider giving it a star ⭐ to show your support.
