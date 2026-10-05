<template>
  <div class="app-wrapper">
    <el-config-provider :locale="lacale" :message="config">
      <div class="common-layout">
        <el-container class="root-container">
          <!-- 自定义标题栏 -->
          <el-header class="title-bar">
            <div class="left-icon no-drag">
              <img
                ref="agtIcon"
                class="icon"
                :src="appIcon"
                @click="playSpin"
              />
            </div>
            <div class="drag-area">
              <button class="title no-drag" @click="showAppInfo">AGT</button>
            </div>
            <!-- Windows style caption buttons -->
            <div class="window-controls no-drag">
              <button
                type="button"
                class="win-btn minimize-btn"
                title="最小化"
                aria-label="最小化"
                @click="minimize"
              >
                <svg viewBox="0 0 10 10" aria-hidden="true">
                  <path d="M0 5h10" />
                </svg>
              </button>
              <button
                type="button"
                class="win-btn maxmize-btn"
                :title="isMaximized ? '向下还原' : '最大化'"
                :aria-label="isMaximized ? '向下还原' : '最大化'"
                @click="maximize"
              >
                <svg v-if="!isMaximized" viewBox="0 0 10 10" aria-hidden="true">
                  <rect x="0.5" y="0.5" width="9" height="9" />
                </svg>
                <svg v-else viewBox="0 0 10 10" aria-hidden="true">
                  <path d="M2.9 0.5h6.6v6.5H7" />
                  <path d="M2.9 0.5v2.5" />
                  <rect x="0.5" y="3" width="6.5" height="6.5" />
                </svg>
              </button>
              <button
                type="button"
                class="win-btn close-btn"
                title="关闭"
                aria-label="关闭"
                @click="close"
              >
                <svg viewBox="0 0 10 10" aria-hidden="true">
                  <path d="M0.5 0.5l9 9M9.5 0.5l-9 9" />
                </svg>
              </button>
            </div>
          </el-header>

          <el-main class="main-window">
            <div v-show="!isResizing">
              <router-view v-slot="{ Component }">
                <keep-alive>
                  <component :is="Component" />
                </keep-alive>
              </router-view>
            </div>
          </el-main>
        </el-container>
      </div>
    </el-config-provider>
  </div>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, onMounted, onBeforeUnmount } from 'vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { ConfirmDialog } from './views/component/comp/confirmDialog.js'
import { useAppCacheData } from './store/app.js';
import { agt_client_version } from './store/globalData.js';
import appIcon from './assets/background/AGT.png'

const lacale = zhCn
const config = ({
  max: 1
})
const { proxy } = getCurrentInstance()
const minimize = () => window.electron.ipcRenderer.send('window-minimize')
const maximize = () => window.electron.ipcRenderer.send('window-maximize')
const isMaximized = ref(false)
let offMaximizedChange = null
async function close() {
  try {
    await ConfirmDialog.confirm(
      `确认要退出程序吗？未保存的数据将会丢失`,
      '关闭确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    window.electron.ipcRenderer.send('window-close')
  } catch {}
}
const store = useAppCacheData()
const agtIcon = ref<HTMLImageElement | null>(null)
function playSpin() {
  const el = agtIcon.value
  if (!el) {
    console.warn("el 为空")
    return
  }
  el.classList.remove('spin')
  void (el as HTMLElement).offsetWidth
  el.classList.add('spin')
  const handler = () => {
    el.classList.remove('spin')
    el.removeEventListener('animationend', handler)
  }
  el.addEventListener('animationend', handler)
}

async function showAppInfo() {
  await ConfirmDialog.confirm(
    '版本: ' + agt_client_version,
    '版本信息',
    {
      confirmButtonText: '确定',
      type: 'info',
    }
  )
}

const isResizing = ref(false)

let resizeTimer: ReturnType<typeof setTimeout> | null = null

function handleWindowResize() {
  isResizing.value = true

  if (resizeTimer) {
    clearTimeout(resizeTimer)
  }

  resizeTimer = setTimeout(() => {
    isResizing.value = false
    resizeTimer = null
  }, 150)
}

onMounted(() => {
  window.addEventListener('resize', handleWindowResize)

  // Sync the caption button with the real window state
  window.api?.isWindowMaximized?.()
    .then((value) => { isMaximized.value = !!value })
    .catch(() => {})

  offMaximizedChange = window.api?.onWindowMaximizedChange?.(
    (value) => { isMaximized.value = !!value }
  ) ?? null
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleWindowResize)

  if (offMaximizedChange) {
    offMaximizedChange()
    offMaximizedChange = null
  }

  if (resizeTimer) {
    clearTimeout(resizeTimer)
    resizeTimer = null
  }
})
</script>

<style scoped>
.app-wrapper {
  background-color: transparent;
}

.app-wrapper {
  position: relative;
  overflow: hidden;
}

.app-wrapper > * {
  position: relative;
  z-index: 1;
}

.top_window {
  padding: 0;
}

.common-layout {
  padding: 0;
}

.root-container {
  padding: 0;
}

.title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  height: 30px;
  padding: 0 0 0 10px;
  color: var(--agt-darkest-color);
  background-color: transparent;
  border-radius: var(--agt-border-radius-base) var(--agt-border-radius-base) 0 0;
  -webkit-app-region: drag;
}

.left-icon {
  display: flex;
  align-items: center;
  width: 20px;
  height: 20px;
}

.icon {
  cursor: pointer;
  display: inline-block;
  transform-origin: 50% 50%;
  width: 20px;
  height: 20px;
  border-radius: var(--agt-border-radius-base);
  object-fit: contain;
  overflow: hidden;
  opacity: 0.7;
  transition: opacity .25s var(--agt-cubic-bezier);
}

.icon:hover {
  opacity: 1;
}

.title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-weight: bold;
  font-size: 14px;
  padding-left: 5px;
  padding-right: 5px;
  color: var(--agt-darkest-color);
  background-color: transparent;
  height: 24px;
  border: none;
}

.drag-area {
  flex: 1;
  display: flex;
  align-items: center;
  border-radius: var(--agt-border-radius-base);
}

.window-controls {
  display: flex;
  align-items: stretch;
  align-self: stretch;
  height: 100%;
  margin-left: auto;
}

.no-drag {
  -webkit-app-region: no-drag; /* 按钮区域不可拖拽 */
  /* color: white; */
}

.win-btn {
  -webkit-app-region: no-drag;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 100%;
  padding: 0;
  margin: 0;
  border: none;
  border-radius: 0;
  background-color: transparent;
  color: inherit;
  cursor: default;
  outline: none;
  transition: background-color .12s ease, color .12s ease;
}

.win-btn svg {
  display: block;
  width: 10px;
  height: 10px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1;
  shape-rendering: crispEdges;
}

.win-btn:hover {
  background-color: rgba(0, 0, 0, 0.08);
}

.win-btn:active {
  background-color: rgba(0, 0, 0, 0.14);
}

/* Windows close button highlights red */
.close-btn:hover {
  background-color: #c42b1c;
  color: #ffffff;
}

.close-btn:active {
  background-color: #b12619;
  color: #ffffff;
}

/* Dark theme */
[data-theme='dark'] .win-btn:hover {
  background-color: rgba(255, 255, 255, 0.10);
}

[data-theme='dark'] .win-btn:active {
  background-color: rgba(255, 255, 255, 0.16);
}

[data-theme='dark'] .close-btn:hover {
  background-color: #c42b1c;
  color: #ffffff;
}

.main-window {
  background-color: transparent;
  padding: 0%;
  border-radius: var(--agt-border-radius-base);
  position: relative;
  min-height: calc(100vh - 30px);
  max-height: calc(100vh - 30px);
}

.icon {
  cursor: pointer;
  display: inline-block;
  transform-origin: 50% 50%;
}

/* 动画类 */
.spin {
  animation: spin-one 800ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes spin-one {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
</style>

