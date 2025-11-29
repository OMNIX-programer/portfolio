from flask import Flask, render_template_string, request

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'


portfolio_data = {
    "name": "OMNIX",
    "title": "python,html,css,js - разработчик",
    "email": "noname@example.com",
    "phone": "+375.........",
    "location": "Беларусь",
    "about": "Я веб-разработчик на Python и JavaScript.А так же делаю тг и дс ботов на Python.",
    "skills": [
        {"name": "Python", "level": 70},
        {"name": "JavaScript", "level": 45},
        {"name": "Flask/Django", "level": 51},
        {"name": "HTML/CSS", "level": 65},
    ],
    "projects": [
        {
            "title": "1",
            "description": "text",
            "technologies": ["programming language"],
            "link": "#"
        },
        {
            "title": "2",
            "description": "text",
            "technologies": ["programming language"],
            "link": "#"
        },
        
    ],
    "experience": [
        {
            "company": "text",
            "position": "text",
            "period": "text",
            "description": "text"
        },
        {
            "company": "text",
            "position": "text",
            "period": "text",
            "description": "text"
        }
    ],
    "education": [
        {
            "institution": "text"
            
        }
    ]
}

# HTML 
SITE_HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Портфолио - {{portfolio_data.name}}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        header {
            background: #2c3e50;
            color: white;
            padding: 1rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: #3498db;
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            transition: color 0.3s;
            font-weight: 500;
        }
        
        .nav-links a:hover {
            color: #3498db;
        }
        
        .hero {
            background: linear-gradient(135deg, #3498db, #2c3e50);
            color: white;
            padding: 150px 0 100px;
            text-align: center;
            margin-top: 60px;
        }
        
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .btn {
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .btn:hover {
            background: #c0392b;
            transform: translateY(-2px);
        }
        
        section {
            padding: 80px 0;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            font-size: 2.5rem;
            color: #2c3e50;
        }
        
        .about-content {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 3rem;
            align-items: center;
        }
        
        .profile-img {
            width: 100%;
            max-width: 300px;
            height: 300px;
            border-radius: 50%;
            background: #3498db;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            margin: 0 auto;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .skill-item {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .skill-name {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        
        .skill-bar {
            background: #ecf0f1;
            border-radius: 10px;
            overflow: hidden;
            height: 10px;
        }
        
        .skill-level {
            background: #3498db;
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-in-out;
        }
        
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }
        
        .project-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .project-card:hover {
            transform: translateY(-5px);
        }
        
        .project-image {
            width: 100%;
            height: 200px;
            background: #bdc3c7;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #2c3e50;
            font-weight: bold;
        }
        
        .project-content {
            padding: 1.5rem;
        }
        
        .project-technologies {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        
        .tech-tag {
            background: #3498db;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
        }
        
        .contact-form {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 0.8rem;
            border: 2px solid #ecf0f1;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .form-group textarea {
            height: 150px;
            resize: vertical;
        }
        
        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem 0;
        }
        
        .experience-item {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        .experience-item h4 {
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .about-content {
                grid-template-columns: 1fr;
                text-align: center;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .nav-links {
                gap: 1rem;
                font-size: 0.9rem;
            }
            
            .profile-img {
                max-width: 250px;
                height: 250px;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav class="container">
            <div class="logo">{{portfolio_data.name}}</div>
            <ul class="nav-links">
                <li><a href="#home">Главная</a></li>
                <li><a href="#about">Обо мне</a></li>
                <li><a href="#skills">Навыки</a></li>
                <li><a href="#projects">Проекты</a></li>
                <li><a href="#contact">Контакты</a></li>
            </ul>
        </nav>
    </header>

    <section id="home" class="hero">
        <div class="container">
            <h1>Привет, я {{portfolio_data.name}}</h1>
            <p>{{portfolio_data.title}}</p>
            <a href="#projects" class="btn">Мои проекты</a>
        </div>
    </section>

    <section id="about">
        <div class="container">
            <h2 class="section-title">Обо мне</h2>
            <div class="about-content">
                <div>
                    <div class="profile-img">
                        Фото профиля
                    </div>
                </div>
                <div>
                    <p style="font-size: 1.1rem; margin-bottom: 2rem; line-height: 1.8;">{{portfolio_data.about}}</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
                        <div>
                            <h4 style="color: #2c3e50; margin-bottom: 1rem;">Контакты</h4>
                            <p><strong>Email:</strong> {{portfolio_data.email}}</p>
                            <p><strong>Телефон:</strong> {{portfolio_data.phone}}</p>
                            <p><strong>Местоположение:</strong> {{portfolio_data.location}}</p>
                        </div>
                        <div>
                            <h4 style="color: #2c3e50; margin-bottom: 1rem;">Образование</h4>
                            {% for edu in portfolio_data.education %}
                            <p><strong>{{edu.institution}}</strong><br>
                            {{edu.degree}}<br>
                            <em>{{edu.period}}</em></p>
                            {% endfor %}
                        </div>
                    </div>
                    
                    <div style="margin-top: 2rem;">
                        <h4 style="color: #2c3e50; margin-bottom: 1rem;">Опыт работы</h4>
                        {% for exp in portfolio_data.experience %}
                        <div class="experience-item">
                            <h4>{{exp.position}} - {{exp.company}}</h4>
                            <p style="color: #7f8c8d; margin-bottom: 0.5rem;">{{exp.period}}</p>
                            <p>{{exp.description}}</p>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="skills" style="background: #ecf0f1;">
        <div class="container">
            <h2 class="section-title">Навыки</h2>
            <div class="skills-grid">
                {% for skill in portfolio_data.skills %}
                <div class="skill-item">
                    <div class="skill-name">
                        <span>{{skill.name}}</span>
                        <span>{{skill.level}}%</span>
                    </div>
                    <div class="skill-bar">
                        <div class="skill-level" style="width: {{skill.level}}%"></div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <section id="projects">
        <div class="container">
            <h2 class="section-title">Мои проекты</h2>
            <div class="projects-grid">
                {% for project in portfolio_data.projects %}
                <div class="project-card">
                    <div class="project-image">
                        Проект: {{project.title}}
                    </div>
                    <div class="project-content">
                        <h3 style="color: #2c3e50; margin-bottom: 1rem;">{{project.title}}</h3>
                        <p style="margin-bottom: 1rem; color: #555;">{{project.description}}</p>
                        <div class="project-technologies">
                            {% for tech in project.technologies %}
                            <span class="tech-tag">{{tech}}</span>
                            {% endfor %}
                        </div>
                        <a href="{{project.link}}" class="btn" style="display: inline-block; margin-top: 1rem;">Подробнее</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <section id="contact" style="background: #ecf0f1;">
        <div class="container">
            <h2 class="section-title">Свяжитесь со мной</h2>
            <div class="contact-form">
                <form action="/contact" method="POST">
                    <div class="form-group">
                        <label for="name">Имя</label>
                        <input type="text" id="name" name="name" required placeholder="Введите ваше имя">
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" name="email" required placeholder="Введите ваш email">
                    </div>
                    <div class="form-group">
                        <label for="message">Сообщение</label>
                        <textarea id="message" name="message" required placeholder="Введите ваше сообщение"></textarea>
                    </div>
                    <button type="submit" class="btn" style="width: 100%;">Отправить сообщение</button>
                </form>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2024 {{portfolio_data.name}}. Все права защищены.</p>
            <p style="margin-top: 1rem; opacity: 0.8;">Email: {{portfolio_data.email}} | Телефон: {{portfolio_data.phone}}</p>
        </div>
    </footer>

    <script>
        // Плавная прокрутка для навигационных ссылок
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Анимация навыков при прокрутке
        function animateSkills() {
            const skills = document.querySelectorAll('.skill-level');
            skills.forEach(skill => {
                const level = skill.style.width;
                skill.style.width = '0';
                setTimeout(() => {
                    skill.style.width = level;
                }, 300);
            });
        }

        // Запуск анимации при загрузке страницы
        window.addEventListener('load', function() {
            setTimeout(animateSkills, 500);
        });

        // Подсветка активного раздела в навигации
        window.addEventListener('scroll', function() {
            const sections = document.querySelectorAll('section');
            const navLinks = document.querySelectorAll('.nav-links a');
            
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (scrollY >= (sectionTop - 100)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(SITE_HTML, portfolio_data=portfolio_data)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    print(f"Новое сообщение от {name} ({email}): {message}")
    
    return render_template_string(SITE_HTML, portfolio_data=portfolio_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
