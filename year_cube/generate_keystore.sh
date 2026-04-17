#!/bin/bash
# 生成 Android 发布签名用的 keystore
# 用法: ./generate_keystore.sh

KEYSTORE_FILE="release.keystore"
KEY_ALIAS="yearcube"
STORE_PASSWORD="yearcube123"
KEY_PASSWORD="yearcube123"

# 如果你要用于正式上架，请把密码改成自己记得住的强密码，并妥善保管此文件！

echo "正在生成 keystore: $KEYSTORE_FILE"

keytool -genkey -v \
  -keystore "$KEYSTORE_FILE" \
  -alias "$KEY_ALIAS" \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass "$STORE_PASSWORD" \
  -keypass "$KEY_PASSWORD" \
  -dname "CN=YearCube, OU=App, O=YearCube, L=City, ST=State, C=CN"

echo ""
echo "=============================================="
echo "Keystore 已生成: $KEYSTORE_FILE"
echo "别名(Alias): $KEY_ALIAS"
echo "Store 密码: $STORE_PASSWORD"
echo "Key 密码: $KEY_PASSWORD"
echo "=============================================="
echo ""
echo "⚠️  警告: 请妥善保管此文件和密码！"
echo "丢失后将无法更新已上架的 App！"
echo ""
echo "本地构建 Release APK 命令:"
echo "  export ANDROID_KEYSTORE_FILE=\$(pwd)/$KEYSTORE_FILE"
echo "  export ANDROID_KEYSTORE_PASSWORD=$STORE_PASSWORD"
echo "  export ANDROID_KEY_ALIAS=$KEY_ALIAS"
echo "  export ANDROID_KEY_PASSWORD=$KEY_PASSWORD"
echo "  cd android && ./gradlew assembleRelease"
echo ""
echo "GitHub Actions 使用步骤:"
echo "  1. 对 keystore 进行 base64 编码:"
echo "     base64 -i $KEYSTORE_FILE | pbcopy"
echo "  2. 在 GitHub 仓库 Settings -> Secrets and variables -> Actions 中添加以下 Secrets:"
echo "     ANDROID_KEYSTORE_BASE64"
echo "     ANDROID_KEYSTORE_PASSWORD"
echo "     ANDROID_KEY_ALIAS"
echo "     ANDROID_KEY_PASSWORD"
