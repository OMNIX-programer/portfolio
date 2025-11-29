from flask import Flask, render_template_string, request, jsonify
from collections import Counter
import re
import os

app = Flask(__name__)

TEXT_ANALYZER_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Анализатор текста</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 { 
            text-align: center; 
            color: #333;
            margin-bottom: 30px;
        }
        .input-area, .results {
            margin-bottom: 30px;
        }
        textarea {
            width: 100%;
            height: 200px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            resize: vertical;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover {
            background: #5a6fd8;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .word-cloud {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 20px;
        }
        .word {
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 14px;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Анализатор текста</h1>
        
        <div class="input-area">
            <textarea id="textInput" placeholder="Введите текст для анализа..."></textarea>
            <button onclick="analyzeText()">Анализировать текст</button>
            <div id="loading" class="loading">Анализируем...</div>
        </div>
        
        <div id="results" class="results" style="display: none;">
            <h2>Результаты анализа</h2>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="charCount">0</div>
                    <div>Символов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="wordCount">0</div>
                    <div>Слов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="sentenceCount">0</div>
                    <div>Предложений</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="readingTime">0</div>
                    <div>Минут чтения</div>
                </div>
            </div>
            
            <h3>Самые частые слова:</h3>
            <div id="wordCloud" class="word-cloud"></div>
            
            <h3>Статистика по длине слов:</h3>
            <div id="wordLengthStats"></div>
        </div>
    </div>

    <script>
        function analyzeText() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                alert('Введите текст для анализа');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            
            fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text: text})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('results').style.display = 'block';
                
                // Обновляем статистику
                document.getElementById('charCount').textContent = data.char_count;
                document.getElementById('wordCount').textContent = data.word_count;
                document.getElementById('sentenceCount').textContent = data.sentence_count;
                document.getElementById('readingTime').textContent = data.reading_time;
                
                // Облако слов
                const wordCloud = document.getElementById('wordCloud');
                wordCloud.innerHTML = '';
                data.top_words.forEach(word => {
                    const wordElement = document.createElement('div');
                    wordElement.className = 'word';
                    wordElement.textContent = `${word[0]} (${word[1]})`;
                    wordCloud.appendChild(wordElement);
                });
                
                // Статистика по длине слов
                const lengthStats = document.getElementById('wordLengthStats');
                lengthStats.innerHTML = '';
                for (const [length, count] of Object.entries(data.word_length_stats)) {
                    const stat = document.createElement('div');
                    stat.textContent = `Слова из ${length} букв: ${count} слов`;
                    stat.style.marginBottom = '5px';
                    lengthStats.appendChild(stat);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loading').style.display = 'none';
            });
        }
        
        // Анализ при вводе текста (опционально)
        document.getElementById('textInput').addEventListener('input', function() {
            if (this.value.length > 1000) {
                analyzeText();
            }
        });
    </script>
</body>
</html>
'''

class TextAnalyzer:
    @staticmethod
    def analyze_text(text):
        # Основная статистика
        char_count = len(text)
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = len(words)
        
        # Подсчет предложений (упрощенный)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Время чтения (средняя скорость 200 слов в минуту)
        reading_time = max(1, round(word_count / 200))
        
        # Самые частые слова
        word_freq = Counter(words)
        stop_words = {'и', 'в', 'на', 'с', 'по', 'для', 'не', 'что', 'это', 'как', 'а', 'но', 'или', 'у', 'о', 'же', 'бы', 'то', 'из'}
        filtered_words = {word: count for word, count in word_freq.items() 
                         if word not in stop_words and len(word) > 2}
        top_words = Counter(filtered_words).most_common(15)
        
        # Статистика по длине слов
        word_lengths = [len(word) for word in words]
        word_length_stats = {}
        for length in word_lengths:
            word_length_stats[length] = word_length_stats.get(length, 0) + 1
        
        return {
            'char_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'reading_time': reading_time,
            'top_words': top_words,
            'word_length_stats': dict(sorted(word_length_stats.items()))
        }

@app.route('/')
def text_analyzer():
    return render_template_string(TEXT_ANALYZER_HTML)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    
    analyzer = TextAnalyzer()
    results = analyzer.analyze_text(text)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)