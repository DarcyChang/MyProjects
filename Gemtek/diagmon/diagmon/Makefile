#
# Copyright (C) 2014 Gemtek
#
# $Id: $

include $(TOPDIR)/rules.mk

PKG_NAME:=diagmon
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk
include $(INCLUDE_DIR)/kernel.mk

define Package/diagmon
  $(call Package/diagmon/Default)
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=Gemtek Diagnostic Tools. (CAP3 project)
  DEPENDS:=+libuci
endef

define Build/Prepare
	$(call Build/Prepare/Default)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
	$(MAKE) -C "$(PKG_BUILD_DIR)" \
		CC="$(TARGET_CC)" \
		LD="$(TARGET_CROSS)ld" \
		LDFLAGS="-L $(PKG_BUILD_DIR) -ldiags -luci"\
		TARGET_CFLAGS="$(TARGET_CFLAGS) -I$(LINUX_DIR)/drivers/char" \
		AR="$(TARGET_CROSS)ar" \
		TOPDIR="$(PKG_BUILD_DIR)" \
		LINUX_DIR="$(LINUX_DIR)"
endef

define Package/diagmon/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/diagmon $(1)/usr/bin/diagmon
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/modules/manufacture/wizard $(1)/usr/bin/wizard
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/modules/button_led/button_led $(1)/usr/bin/button_led
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/modules/cpu/cpu $(1)/usr/bin/cpu
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/modules/usbtest/usbtest $(1)/usr/bin/usbtest
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/modules/sdtest/sdtest $(1)/usr/bin/sdtest
endef

define Build/Clean
    if [ -d $(PKG_BUILD_DIR) ]; then $(MAKE) -C $(PKG_BUILD_DIR) clean; \
    $(RM) -r $(PKG_BUILD_DIR)/ipkg-$(BOARD); fi
endef


$(eval $(call BuildPackage,diagmon))
