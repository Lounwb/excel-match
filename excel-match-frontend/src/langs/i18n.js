import { createI18n } from 'vue-i18n'
import messages from './langs'

//从localStorage获取语言选择。
const i18n = createI18n({
    legacy:false,
    locale:localStorage.getItem('lang') || 'zh',//语言包
    messages
})

export default i18n
