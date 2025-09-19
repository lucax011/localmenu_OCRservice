pipeline {
    agent any
    environment {
        APP_PORT = '8000'
        EXTRACTOR_ENGINE = 'tesseract'
        ENABLE_PREPROCESSING = 'true'
        RETURN_BBOXES = 'true'
        MAX_UPLOAD_MB = '10'
    }
    stages {
        stage('Setup') {
            steps {
                cache(path: 'venv', key: 'pip')
                sh 'python -m venv venv && . venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Lint') {
            steps {
                sh '. venv/bin/activate && ruff src && black --check src && isort --check src'
            }
        }
        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest --maxfail=1 --disable-warnings'
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t localmenu_ocrservice .'
            }
        }
        stage('Integration Test') {
            steps {
                sh 'docker-compose up -d'
                sh 'sleep 10'
                sh 'curl -f http://localhost:8000/health'
                sh 'curl -f -F "file=@tests/assets/menu1.jpg" http://localhost:8000/ocr/extract'
                sh 'curl -f -F "file=@tests/assets/menu2.jpg" http://localhost:8000/ocr/extract'
                sh 'docker-compose down'
            }
        }
        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'logs/**, coverage.xml', allowEmptyArchive: true
            }
        }
    }
}
