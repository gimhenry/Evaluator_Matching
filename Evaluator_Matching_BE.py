from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import geodesic

# Flask 앱 정의
app = Flask(__name__)

# SQLAlchemy 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaluators.db'
db = SQLAlchemy(app)

# 모델 정의
class Evaluator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    max_requests = db.Column(db.Integer, default=5)
    current_requests = db.Column(db.Integer, default=0)

# 데이터베이스 초기화 함수
def initialize_database():
    with app.app_context():  # Flask 애플리케이션 컨텍스트 생성
        db.create_all()
        if not Evaluator.query.first():
            db.session.add(Evaluator(name="Evaluator 1", location="37.5651,126.9895", max_requests=5))
            db.session.add(Evaluator(name="Evaluator 2", location="37.5510,126.9882", max_requests=3))
            db.session.commit()

# 기본 라우트
@app.route("/")
def home():
    return "Hello, Flask!"

# 평가사 매칭 API
@app.route('/assign', methods=['POST'])
def assign_evaluator():
    data = request.json
    customer_location = tuple(map(float, data['location']))  # [lat, lon]

    # 평가사 필터링 및 거리 계산
    evaluators = Evaluator.query.all()
    available_evaluators = [
        e for e in evaluators if e.current_requests < e.max_requests
    ]
    if not available_evaluators:
        return jsonify({"error": "No available evaluators"}), 400

    # 최적 평가사 찾기
    best_evaluator = min(
        available_evaluators,
        key=lambda e: geodesic(customer_location, tuple(map(float, e.location.split(",")))).kilometers
    )

    # 결과 반환
    return jsonify({
        "assigned_evaluator": best_evaluator.id,
        "distance": geodesic(customer_location, tuple(map(float, best_evaluator.location.split(",")))).kilometers
    })



from waitress import serve

if __name__ == "__main__":
    # 데이터베이스 초기화
    initialize_database()
    # Waitress를 사용해 애플리케이션 실행
    serve(app, host="0.0.0.0", port=5000)
