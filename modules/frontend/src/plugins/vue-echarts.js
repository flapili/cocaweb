import Vue from 'vue'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'


import { CanvasRenderer } from 'echarts/renderers'
import { GridComponent, TooltipComponent, TitleComponent, LegendComponent } from 'echarts/components'

// charts
import { PieChart, LineChart } from 'echarts/charts'

use([
    CanvasRenderer,
    GridComponent,
    TooltipComponent,
    TitleComponent,
    LegendComponent,

    // charts
    PieChart,
    LineChart,
]);

Vue.component('v-chart', ECharts)