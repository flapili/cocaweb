<template >
  <div v-loading.fullscreen.lock="$fetchState.pending">
    <template v-if="guild && guild.id && guild.icon">
      <el-row>
        <el-col :xs="{ span: 12, offset: 6 }" :md="{ span: 2, offset: 11 }">
          <img
            :src="`https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.webp`"
            alt="icone de la guilde"
            style="width: 100%; height: 100%; border-radius: 10px"
          />
        </el-col>
      </el-row>

      <el-row type="flex" justify="center" style="margin-bottom: 30px">
        <el-col :md="4" style="text-align: center">
          <h2>{{ member_count.toLocaleString() }} membres actifs !</h2>
          <h2>{{ message_count.toLocaleString() }} messages !</h2>
        </el-col>
      </el-row>
    </template>

    <el-row style="margin-bottom: 30px" :gutter="10">
      <el-col :md="{ span: 4, offset: 6 }" :xs="{ span: 20, offset: 2 }">
        <el-date-picker v-model="after" type="datetime" class="datepicker" />
      </el-col>
      <el-col :md="4" :xs="{ span: 20, offset: 2 }">
        <el-date-picker v-model="before" type="datetime" class="datepicker" />
      </el-col>
      <el-col :md="4" :xs="{ span: 20, offset: 2 }">
        <el-button
          style="width: 100%"
          :loading="$fetchState.pending"
          @click="$fetch"
        >
          Rechercher
        </el-button>
      </el-col>
    </el-row>

    <el-row
      type="flex"
      justify="center"
      v-if="!$fetchState.pending && !$fetchState.error"
    >
      <el-col :md="12">
        <el-card style="border-radius: 30px">
          <el-collapse style="width: 100%">
            <el-collapse-item
              v-for="(user, i) in users.slice(
                (currentPage - 1) * perPage,
                currentPage * perPage
              )"
              :key="i"
              :name="i"
              class="parent"
              :class="{ 'not-member': !user.joined_at }"
            >
              <template slot="title">
                <div class="user-container">
                  <div
                    class="rank"
                    :style="{
                      backgroundColor: backgroundColorRank(
                        i + (currentPage - 1) * perPage
                      ),
                      color:
                        i + (currentPage - 1) * perPage < 3 ? 'black' : 'white',
                    }"
                  >
                    <span>{{ i + (currentPage - 1) * perPage + 1 }}</span>
                  </div>

                  <img
                    :src="
                      $common.get_avatar(
                        user.id,
                        user.discriminator,
                        user.avatar
                      )
                    "
                    :alt="`avatar de ${user.username}`"
                    class="avatar"
                  />
                </div>
                <div style="margin-left: 20px">
                  <h3>{{ user.username }}#{{ user.discriminator }}</h3>
                </div>
                <div style="margin-left: auto">
                  {{ user.total_messages.toLocaleString() }}
                </div>
              </template>

              <template>
                <div>
                  Compte créé le :<br />
                  {{ new Date(user.created_at).toLocaleString() }}
                  <el-divider />
                </div>
                <div v-if="user.display_name">{{ user.display_name }}</div>
                <div v-if="user.joined_at">
                  à rejoint le serveur le :<br />
                  {{ new Date(user.joined_at).toLocaleString() }}
                  <el-divider />
                </div>
                <div
                  v-for="(channel, indexChannel) in user.channels"
                  :key="indexChannel"
                >
                  <a
                    :href="`https://discord.com/channels/${guild.id}/${channel.id}`"
                    target="_blank"
                    rel="nofollow noopener"
                    class="channel-link"
                    >#{{ channel.name }}
                  </a>
                  : {{ channel.count.toLocaleString() }}
                </div>
              </template>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-col>
    </el-row>

    <el-pagination
      style="display: flex; justify-content: center; margin-top: 20px"
      layout="prev, pager, next, sizes"
      background
      :hide-on-single-page="true"
      :total="users.length"
      :page-size.sync="perPage"
      :page-sizes="[20, 50, 100, 200, 500]"
      :current-page.sync="currentPage"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      after: null,
      before: null,
      users: [],
      guild: {},
      currentPage: 1,
      perPage: 20,
    };
  },

  computed: {
    member_count() {
      return this.users.filter((u) => u.joined_at).length;
    },
    message_count() {
      return this.users.reduce((acc, u) => acc + u.total_messages, 0);
    },
  },

  methods: {
    backgroundColorRank(rank) {
      if (rank == 0) {
        return "gold";
      } else if (rank == 1) {
        return "silver";
      } else if (rank == 2) {
        return "#cd7f32";
      } else {
        return "#23272A";
      }
    },
  },

  async fetch() {
    const params = { guild_id: "532970830246707244" };
    if (this.after) {
      params.after = this.after;
    }
    if (this.before) {
      params.before = this.before;
    }
    const data = await this.$api.$get("/discord_stats/leaderboard", {
      params: params,
    });
    this.guild = data.partial_guild;
    data.users.sort((a, b) => +b.total_messages - +a.total_messages);
    data.users.forEach((user) => {
      user.channels.sort((a, b) => +b.count - +a.count);
    });
    this.users = data.users;
  },
};
</script>

<style scoped>
.user-container {
  display: flex;
  align-items: center;
}

.rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  margin-right: 15px;
  margin-left: 15px;
}

.avatar {
  height: 60px;
  width: 60px;
  border-radius: 50%;
}

.channel-link {
  background-color: #7289da;
  border-radius: 3px;
  text-decoration: none;
  color: white;
}
</style>

<style>
.datepicker {
  width: 100% !important;
}

div.parent > div > div.el-collapse-item__header {
  height: 80px;
}

div.parent.not-member > div > div.el-collapse-item__header {
  background-color: lightgrey;
  border-radius: 5px;
}

div.parent > div > div.el-collapse-item__wrap > div.el-collapse-item__content {
  font-size: 1rem;
}

div.parent > div > div.el-collapse-item__header > i.el-collapse-item__arrow {
  margin: unset;
}
</style>