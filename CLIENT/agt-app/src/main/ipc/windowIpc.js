import { ipcMain, app } from 'electron'
import { isWin } from '../app/constants'

export function registerWindowIpc(win) {
  console.log('registerWindowIpc...')
  ipcMain.on('window-minimize', () => win.minimize())

  ipcMain.on('window-maximize', () => {
    win.isMaximized() ? win.unmaximize() : win.maximize()
  })

  ipcMain.on('window-close', () => {
    isWin ? win.close() : app.quit()
  })

  // Keep the renderer caption button in sync with the real window state.
  // Covers Aero snap, double-click on the drag area, Win+Arrow, ...
  win.on('maximize', () => {
    if (!win.webContents.isDestroyed()) {
      win.webContents.send('window-maximized-changed', true)
    }
  })

  win.on('unmaximize', () => {
    if (!win.webContents.isDestroyed()) {
      win.webContents.send('window-maximized-changed', false)
    }
  })

  // Guard against duplicate registration when the window is recreated.
  ipcMain.removeHandler('window:is-maximized')
  ipcMain.handle('window:is-maximized', () => win.isMaximized())
}
