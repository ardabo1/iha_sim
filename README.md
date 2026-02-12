## 📋 Ön Gereksinimler

Bu projeyi çalıştırmadan önce sisteminizde aşağıdakilerin kurulu olması gerekir:

* **Ubuntu 22.04 LTS**
* **ROS 2 Humble**
* **Gazebo Harmonic** (Fortress değil!)
* **ArduPilot** (SITL ve MAVProxy)
* **ros_gz_bridge** (ROS 2 ve Gazebo haberleşmesi için)

> 💡 **Kurulum Scriptleri:** Eğer sisteminiz hazır değilse, bu reponun içindeki `scripts/` (veya ana dizindeki) kurulum dosyalarını kullanarak ortamı hazırlayabilirsiniz.

---

## 🚀 Kurulum Adımları

### 1. Projeyi Klonlayın
Terminali açın ve ROS 2 çalışma alanınızın `src` klasörüne gidin:

```bash
cd ~/ros2_ws/src
git clone [https://github.com/ardabo1/uav-sim.git](https://github.com/ardabo1/uav-sim.git)

```

### 2. Bağımlılıkları Yükleyin ve Derleyin

Ana çalışma alanına dönüp paketi derleyin:

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash

```

### 3. Gazebo Harmonic Ayarı (⚠️ ÇOK ÖNEMLİ)

ROS 2 Humble, varsayılan olarak eski Gazebo sürümünü arar. Harmonic kullandığımızı sisteme tanıtmak için şu komutu **mutlaka** çalıştırın (bunu `.bashrc` dosyanıza eklemeniz önerilir):

```bash
export GZ_VERSION=harmonic

```

### 4. ArduPilot Frame ve Ayar Kurulumu

Bu projede **özel bir İHA gövdesi (frame)** kullanılmaktadır. ArduPilot'un bu frame'i tanıması için hazırladığımız scripti çalıştırın:

```bash
cd ~/ros2_ws/src/iha_sim
chmod +x setup_ardupilot_frame.sh
./setup_ardupilot_frame.sh

```

*Bu işlem, gerekli parametre dosyalarını ve `vehicleinfo.py` dosyasını ArduPilot klasörünüze otomatik kopyalar.*

---

## 🎮 Simülasyonu Başlatma

Simülasyonu tam olarak çalıştırmak için iki farklı terminale ihtiyacınız var.

### Terminal 1: Gazebo ve ROS 2 Ortamı

Dünyayı ve fizik motorunu başlatır:

```bash
cd ~/ros2_ws
source install/setup.bash
export GZ_VERSION=harmonic
ros2 launch iha_sim sim_start.launch.py

```

### Terminal 2: ArduPilot SITL

Otopilot yazılımını başlatır ve İHA'yı kontrol eder:

```bash
# ArduPilot dizininde (veya path'e ekli ise her yerden):
sim_vehicle.py -v ArduPlane -f gazebo-minitalon --model JSON --console --map

```

*(Not: `-f gazebo-minitalon` parametresi, yukarıdaki kurulum scripti ile eklediğimiz özel frame'dir.)*

---

## 📂 Klasör Yapısı

* **launch/**: ROS 2 başlatma dosyaları (`sim_start.launch.py`).
* **models/**: İHA ve çevre modelleri (SDF formatında).
* **worlds/**: Gazebo dünya dosyaları (`sim.sdf`).
* **config/**: ArduPilot için özel parametre ve frame dosyaları.
* **scripts/**: Kurulum ve yapılandırma scriptleri.

---

## 🛠️ Sık Karşılaşılan Sorunlar

**1. "Package 'ros_gz_sim' not found" Hatası:**

* `sudo apt install ros-humble-ros-gz` komutuyla paketin kurulu olduğundan emin olun.
* `export GZ_VERSION=harmonic` komutunu girdiğinizden emin olun.

**2. ArduPilot Frame Hatası:**

* SITL başlatırken "Unknown frame" hatası alıyorsanız, `./setup_ardupilot_frame.sh` scriptini tekrar çalıştırın ve `~/ardupilot` dizininin doğru yerde olduğundan emin olun.

**3. Görüntü Gelmiyor / Topic Yok:**

* Gazebo Harmonic topicleri otomatik olarak ROS 2'ye aktarılmaz. Launch dosyasındaki `ros_gz_bridge` ayarlarını kontrol edin.

---
