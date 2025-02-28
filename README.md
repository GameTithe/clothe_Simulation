# 🏗️ Taichi Cloth Simulation

## 📌 프로젝트 개요
이 프로젝트는 **Taichi** 프레임워크를 사용하여 **천이 공 위에 떨어지는 물리 시뮬레이션**을 구현한 것입니다.  
천(Cloth)은 **질량-스프링 시스템(Mass-Spring System)** 으로 모델링되었으며,  
실시간 충돌 감지 및 **GPU 가속을 통한 빠른 시뮬레이션**이 가능합니다.  

## 🚀 주요 기능
- ✅ **Taichi 기반 Cloth Simulation**
- ✅ **GPU 가속 지원 (빠른 시뮬레이션)**
- ✅ **질량-스프링 시스템 적용 (Mass-Spring System)**
- ✅ **공과의 충돌 처리 (Elastic Collision)**
- ✅ **Taichi GGUI 기반 3D 렌더링**
- ✅ **공 개수 및 크기 조정 가능**

---

## 🔧 설치 방법

### 1️⃣ **Python 환경 설정**
Taichi를 사용하기 위해 **Python 3.8 이상**이 필요합니다.  
아래 명령어를 실행하여 **Python 가상 환경을 설정할 수 있습니다.**
```bash
python -m venv taichi_env
source taichi_env/bin/activate  # Windows에서는 `taichi_env\Scripts\activate`
