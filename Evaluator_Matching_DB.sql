-- 고객 테이블
CREATE TABLE Customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location GEOGRAPHY(Point, 4326),
    request_time TIMESTAMP
);

-- 평가사 테이블
CREATE TABLE Evaluators (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location GEOGRAPHY(Point, 4326),
    max_requests INT,
    current_requests INT DEFAULT 0,
    available_times JSONB
);

-- 요청 테이블
CREATE TABLE Requests (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customers(id),
    evaluator_id INT REFERENCES Evaluators(id),
    status VARCHAR(50) DEFAULT 'pending',
    assigned_at TIMESTAMP
);
