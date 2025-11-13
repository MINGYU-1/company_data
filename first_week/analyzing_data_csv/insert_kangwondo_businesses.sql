-- 사용할 데이터베이스 선택: USE your_database;


DROP TABLE IF EXISTS kangwondo_businesses;
CREATE TABLE kangwondo_businesses (
    연번 INT,
    시도 VARCHAR(50),
    시군구 VARCHAR(50),
    업태 VARCHAR(100),
    주메뉴 VARCHAR(255),
    업소명 VARCHAR(255),
    주소 VARCHAR(255),
    최초_지정일자 VARCHAR(50)
);

INSERT INTO kangwondo_businesses (연번, 시도, 시군구, 업태, 주메뉴, 업소명, 주소, 최초 지정일자) VALUES
