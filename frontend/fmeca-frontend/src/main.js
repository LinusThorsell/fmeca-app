import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueResizeObserver from "vue-resize-observer"
import JsonViewer from 'vue-json-viewer'

// import "./assets/main.css";

const app = createApp(App);

app.use(router);
app.use(VueResizeObserver);
app.use(JsonViewer);
app.config.globalProperties.$log = console.log

app.mount("#app");
