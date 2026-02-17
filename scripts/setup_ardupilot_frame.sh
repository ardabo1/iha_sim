#!/bin/bash

# ArduPilot varsayılan dizini (Genelde home dizinindedir)
ARDUPILOT_DIR=~/ardupilot

# Renkli çıktılar için
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}--- Özel İHA Frame Kurulumu Başlıyor ---${NC}"

# 1. ArduPilot kurulu mu kontrol et
if [ ! -d "$ARDUPILOT_DIR" ]; then
    echo "HATA: ArduPilot klasörü ($ARDUPILOT_DIR) bulunamadı!"
    echo "Lütfen ArduPilot'u home dizinine kurduğunuzdan emin olun."
    exit 1
fi

# 2. Frame dosyasını (parametreleri) kopyala
# SITL parametrelerinin olduğu yer: Tools/autotest/default_params/
echo "1. 'gazebo-minitalon.parm' parametre dosyası kopyalanıyor..."
cp config/gazebo-minitalon.parm $ARDUPILOT_DIR/Tools/autotest/default_params/

# 3. vehicleinfo.py dosyasını güncelle
# Bu dosya şurada durur: Tools/autotest/pysim/
DEST_INFO_PATH=$ARDUPILOT_DIR/Tools/autotest/pysim/vehicleinfo.py

echo "2. vehicleinfo.py güncelleniyor..."

# Önce orijinal dosyanın yedeğini alalım (Güvenlik için)
if [ ! -f "$DEST_INFO_PATH.bak" ]; then
    echo "   Orijinal dosya yedekleniyor (vehicleinfo.py.bak)..."
    cp $DEST_INFO_PATH "$DEST_INFO_PATH.bak"
fi

# Senin dosyanı üzerine yaz
cp config/vehicleinfo.py $DEST_INFO_PATH

echo -e "${GREEN}--- Kurulum Başarıyla Tamamlandı! ---${NC}"
echo "Artık şu komutla simülasyonu başlatabilirsiniz:"
echo "sim_vehicle.py -v ArduPlane -f gazebo-minitalon --model JSON --add-param-file=$ARDUPILOT_DIR/Tools/autotest/default_params/gazebo-minitalon.parm"
