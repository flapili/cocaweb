<template>
  <div v-loading.fullscreen.lock="$fetchState.pending">
    <template>
      <el-row style="margin-bottom: 30px" :gutter="10">
        <el-col :md="{ span: 4, offset: 6 }" :sm="{ span: 20, offset: 2 }">
          <el-date-picker v-model="after" type="datetime" class="datepicker" />
        </el-col>
        <el-col :md="{ span: 4, offset: 0 }" :sm="{ span: 20, offset: 2 }">
          <el-date-picker v-model="before" type="datetime" class="datepicker" />
        </el-col>
        <el-col :md="{ span: 4, offset: 0 }" :sm="{ span: 20, offset: 2 }">
          <el-button style="width: 100%" @click="$fetch">
            Rechercher
          </el-button>
        </el-col>
      </el-row>
      <el-row>
        <template
          v-if="
            data_total.x_axis &&
            data_total.x_axis.length &&
            data_total.series &&
            data_total.series.length
          "
        >
          <el-col>
            <h1 style="text-align: center">Activité de la guilde</h1>
            <v-chart style="min-height: 600px" :option="option" autoresize />
            <el-switch v-model="cumSum" active-text="Somme cumulative" />
          </el-col>
        </template>
        <template v-else>
          <h1 style="text-align: center">Aucune donnée</h1>
        </template>
      </el-row>
    </template>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data_total: {},
      after: null,
      before: null,
      cumSum: false,
    };
  },
  computed: {
    option() {
      if (!this.data_total.x_axis || !this.data_total.series) {
        return {};
      }
      const copy = JSON.parse(JSON.stringify(this.data_total));
      return {
        title: {
          show: false,
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
            },
          },
        },
        legend: {
          data: copy.series.map((serie) => serie.name),
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: copy.x_axis.map((x) => new Date(x).toLocaleString()),
          axisLabel: {
            rotate: "5",
            fontWeight: "bold",
            color: "black",
          },
        },
        yAxis: {
          type: "value",
          axisLabel: {
            fontWeight: "bold",
            color: "black",
          },
        },
        series: copy.series.map((serie) => {
          serie.type = "line";
          serie.stack = "total";
          serie.symbol = "none";
          serie.areaStyle = {};
          if (this.cumSum) {
            let acc = 0;
            serie.data = serie.data.map((value) => (acc += value));
          }
          return serie;
        }),
      };
    },
  },

  async fetch() {
    const params = { guild_id: "532970830246707244", intervals: 200 };
    if (this.after) {
      params.after = this.after;
    }
    if (this.before) {
      params.before = this.before;
    }
    this.data_total = await this.$api.$get(
      "/discord_stats/messages_per_channel",
      {
        params: params,
      }
    );
  },
};
</script>