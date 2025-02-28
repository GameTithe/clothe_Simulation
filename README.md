🚀 README 한글 버전 (Taichi Cloth Simulation)
📌 주요 기능
✅ Taichi를 활용한 실시간 Cloth Simulation
✅ 질량-스프링 시스템(Mass-Spring System) 기반 물리 연산
✅ GPU 가속을 활용하여 빠른 시뮬레이션 및 렌더링
✅ 공과의 충돌(Elastic Collision) 처리
✅ Taichi GGUI를 활용한 3D 렌더링

📌 프로젝트 개요
이 프로젝트는 Taichi 프레임워크를 사용하여 천이 공 위에 떨어지는 물리 시뮬레이션을 구현한 것입니다.
천(Cloth)은 질량-스프링 시스템(Mass-Spring System) 으로 모델링되었으며,
실시간 충돌 감지 및 GPU 가속을 통한 빠른 시뮬레이션이 가능합니다.

📌 설치 방법
1️⃣ Python 환경 설정
Taichi를 사용하기 위해 Python 3.8 이상이 필요합니다.
아래 명령어를 실행하여 Python 가상 환경을 설정할 수 있습니다.

bash
복사
편집
python -m venv taichi_env
source taichi_env/bin/activate  # (Windows에서는 `taichi_env\Scripts\activate` 실행)
2️⃣ Taichi 및 필수 라이브러리 설치
bash
복사
편집
pip install taichi
또는 GPU 지원이 필요할 경우:

bash
복사
편집
pip install taichi-gpu
📌 실행 방법
bash
복사
편집
python mpm.py
실행하면 시뮬레이션 창이 열리며, 천(Cloth)이 공 위에 떨어지는 모습을 볼 수 있습니다.

📌 코드 설명
1️⃣ 질량-스프링 시스템 초기화
python
복사
편집
x = ti.Vector.field(3, dtype=float, shape=(n, n))  # 질량점의 위치
v = ti.Vector.field(3, dtype=float, shape=(n, n))  # 질량점의 속도
quad_size = 1.0 / n
x: 각 질량점의 위치를 저장하는 필드
v: 각 질량점의 속도를 저장하는 필드
quad_size: 천을 구성하는 격자의 크기 설정
2️⃣ 공 정보 설정
python
복사
편집
balls_count = 2  
balls_radius = ti.field(dtype=float, shape=balls_count)
balls_center = ti.Vector.field(3, dtype=float, shape=balls_count)
balls_center: 공의 위치 정보 저장
balls_radius: 공의 반지름 정보 저장
3️⃣ 중력 및 물리 법칙 적용
python
복사
편집
gravity = ti.Vector([0, -9.8, 0])  # 중력 가속도
spring_Y = 3e4  # 스프링 강성 계수
dashpot_damping = 1e4  # 감쇠 계수
drag_damping = 1  # 공기 저항
spring_Y: 스프링 강성을 설정하여 천이 늘어나는 정도 결정
dashpot_damping: 감쇠 계수를 통해 천의 움직임이 부드럽게 감소하도록 설정
4️⃣ 충돌 감지 및 반응
python
복사
편집
for i in ti.grouped(x):
    for j in range(balls_count):
        offset_to_center = x[i] - balls_center[j]
        if offset_to_center.norm() <= balls_radius[j]:  # 공과 충돌 감지
            normal = offset_to_center.normalized()
            v[i] -= min(v[i].dot(normal), 0) * normal  # 탄성 충돌 적용
offset_to_center.norm() <= balls_radius[j]를 통해 공과의 충돌 여부 확인
탄성 충돌을 적용하여 반사 효과 구현
📌 시뮬레이션 화면
천이 공 위로 떨어지는 모습
📌 추가 기능
📌 1️⃣ 공의 개수를 원하는 만큼 늘릴 수 있음
📌 2️⃣ 천의 크기 및 해상도를 조절 가능
📌 3️⃣ 파티클 시스템을 이용해 다른 물리 시뮬레이션에도 적용 가능

📌 라이선스
이 프로젝트는 MIT 라이선스를 따르며, 자유롭게 수정 및 배포할 수 있습니다.
문의 사항이나 개선 제안이 있다면 이슈를 등록하거나 PR을 보내주세요! 🚀

📌 최종 정리
✅ Taichi 기반 Cloth Simulation 🚀
✅ 실시간 GPU 가속 지원
✅ 탄성 충돌 및 질량-스프링 시스템 적용
✅ 사용자 지정 가능 (공 개수, 천 크기 조절 가능)

💡 궁금한 점이 있다면 언제든지 질문해주세요! 🎯
