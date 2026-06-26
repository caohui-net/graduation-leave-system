/**
 * 响应式适配器 - 移动端自动适配模块
 * @version 1.0.0
 * @description 自动检测设备类型和屏幕尺寸，动态调整UI
 * @license MIT
 */

(function(global) {
  'use strict';

  // 屏幕尺寸分类标准
  const BREAKPOINTS = {
    xs: 360,   // 超小屏（老款手机）
    sm: 480,   // 小屏（手机竖屏）
    md: 768,   // 中屏（手机横屏/小平板）
    lg: 1024,  // 大屏（平板）
    xl: 1280   // 超大屏（桌面）
  };

  // 设备类型枚举
  const DEVICE_TYPES = {
    MOBILE: 'mobile',
    TABLET: 'tablet',
    DESKTOP: 'desktop'
  };

  class ResponsiveAdapter {
    constructor(options = {}) {
      this.options = {
        breakpoints: { ...BREAKPOINTS, ...options.breakpoints },
        rootElement: options.rootElement || document.documentElement,
        classPrefix: options.classPrefix || 'screen-',
        enableAutoClass: options.enableAutoClass !== false,
        enableResize: options.enableResize !== false,
        debounceDelay: options.debounceDelay || 150
      };

      this.currentScreen = null;
      this.currentDevice = null;
      this.listeners = {};

      this._init();
    }

    // 初始化
    _init() {
      this._updateState();

      if (this.options.enableResize) {
        window.addEventListener('resize', this._debounce(() => {
          this._updateState();
        }, this.options.debounceDelay));
      }
    }

    // 更新设备状态
    _updateState() {
      const oldScreen = this.currentScreen;
      const oldDevice = this.currentDevice;

      this.currentScreen = this.getScreenSize();
      this.currentDevice = this.getDeviceType();

      if (this.options.enableAutoClass) {
        this._updateClasses();
      }

      // 触发变化事件
      if (oldScreen !== this.currentScreen) {
        this._emit('screenChange', {
          from: oldScreen,
          to: this.currentScreen,
          width: this.getWidth()
        });
      }

      if (oldDevice !== this.currentDevice) {
        this._emit('deviceChange', {
          from: oldDevice,
          to: this.currentDevice
        });
      }
    }

    // 更新CSS类名
    _updateClasses() {
      const root = this.options.rootElement;
      const prefix = this.options.classPrefix;

      // 移除旧类名
      root.className = root.className.replace(
        new RegExp(`${prefix}\\w+`, 'g'),
        ''
      ).trim();

      // 添加新类名
      root.classList.add(`${prefix}${this.currentScreen}`);
      root.classList.add(`device-${this.currentDevice}`);
    }

    // 防抖函数
    _debounce(func, delay) {
      let timer;
      return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
      };
    }

    // 事件发射
    _emit(event, data) {
      if (this.listeners[event]) {
        this.listeners[event].forEach(callback => callback(data));
      }
    }

    // 获取屏幕宽度
    getWidth() {
      return window.innerWidth;
    }

    // 获取屏幕高度
    getHeight() {
      return window.innerHeight;
    }

    // 获取屏幕尺寸分类
    getScreenSize() {
      const width = this.getWidth();
      const bp = this.options.breakpoints;

      if (width <= bp.xs) return 'xs';
      if (width <= bp.sm) return 'sm';
      if (width <= bp.md) return 'md';
      if (width <= bp.lg) return 'lg';
      return 'xl';
    }

    // 获取设备类型
    getDeviceType() {
      const width = this.getWidth();
      const bp = this.options.breakpoints;

      if (width <= bp.md) return DEVICE_TYPES.MOBILE;
      if (width <= bp.lg) return DEVICE_TYPES.TABLET;
      return DEVICE_TYPES.DESKTOP;
    }

    // 判断是否为移动设备
    isMobile() {
      return this.currentDevice === DEVICE_TYPES.MOBILE;
    }

    // 判断是否为平板
    isTablet() {
      return this.currentDevice === DEVICE_TYPES.TABLET;
    }

    // 判断是否为桌面
    isDesktop() {
      return this.currentDevice === DEVICE_TYPES.DESKTOP;
    }

    // 判断是否为触摸设备
    isTouchDevice() {
      return 'ontouchstart' in window ||
             navigator.maxTouchPoints > 0 ||
             navigator.msMaxTouchPoints > 0;
    }

    // 获取操作系统
    getOS() {
      const ua = navigator.userAgent;
      if (/iPhone|iPad|iPod/.test(ua)) return 'iOS';
      if (/Android/.test(ua)) return 'Android';
      if (/Windows/.test(ua)) return 'Windows';
      if (/Mac/.test(ua)) return 'MacOS';
      if (/Linux/.test(ua)) return 'Linux';
      return 'Unknown';
    }

    // 判断是否为iOS
    isIOS() {
      return this.getOS() === 'iOS';
    }

    // 判断是否为Android
    isAndroid() {
      return this.getOS() === 'Android';
    }

    // 获取设备像素比
    getPixelRatio() {
      return window.devicePixelRatio || 1;
    }

    // 判断是否为高清屏
    isRetina() {
      return this.getPixelRatio() >= 2;
    }

    // 监听事件
    on(event, callback) {
      if (!this.listeners[event]) {
        this.listeners[event] = [];
      }
      this.listeners[event].push(callback);
      return this;
    }

    // 移除监听
    off(event, callback) {
      if (!this.listeners[event]) return this;

      if (callback) {
        this.listeners[event] = this.listeners[event].filter(
          cb => cb !== callback
        );
      } else {
        delete this.listeners[event];
      }
      return this;
    }

    // 获取完整设备信息
    getDeviceInfo() {
      return {
        screen: this.currentScreen,
        device: this.currentDevice,
        width: this.getWidth(),
        height: this.getHeight(),
        os: this.getOS(),
        isTouch: this.isTouchDevice(),
        pixelRatio: this.getPixelRatio(),
        isRetina: this.isRetina()
      };
    }
  }

  // 单例模式
  let instance = null;

  // 导出工厂函数
  const createAdapter = (options) => {
    if (!instance) {
      instance = new ResponsiveAdapter(options);
    }
    return instance;
  };

  // 快速访问方法
  const quickAPI = {
    isMobile: () => instance?.isMobile() || window.innerWidth <= 768,
    isTablet: () => instance?.isTablet() ||
                    (window.innerWidth > 768 && window.innerWidth <= 1024),
    isDesktop: () => instance?.isDesktop() || window.innerWidth > 1024,
    getWidth: () => window.innerWidth,
    getHeight: () => window.innerHeight
  };

  // 导出到全局
  global.ResponsiveAdapter = {
    create: createAdapter,
    getInstance: () => instance,
    ...quickAPI
  };

  // 兼容CommonJS
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = global.ResponsiveAdapter;
  }

})(typeof window !== 'undefined' ? window : this);
