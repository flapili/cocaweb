<template>
  <el-container>
    <el-header>
      <nuxt-link to="/" class="header-link">
        <font-awesome-icon
          :icon="['fas', 'home']"
          size="2x"
          style="color: white"
        />
      </nuxt-link>

      <nuxt-link to="/leaderboard" class="header-link">
        <font-awesome-icon
          :icon="['fas', 'chart-line']"
          size="2x"
          style="color: white"
        />
      </nuxt-link>

      <el-tooltip placement="bottom-end">
        <div
          slot="content"
          v-if="!$fetchState.pending && !$fetchState.error"
          class="avatar-popup"
        >
          {{ me.username }}#{{ me.discriminator }}<br />
          {{ me.display_name }}<br />
          membre depuis :<br />
          {{ new Date(me.joined_at).toLocaleString() }}<br />
          <el-button type="danger" @click="disconnect">
            <font-awesome-icon :icon="['fas', 'sign-out-alt']" />
          </el-button>
        </div>
        <div
          slot="content"
          v-else-if="$fetchState.pending"
          class="avatar-popup"
        >
          Loading ...
        </div>
        <div slot="content" v-else class="avatar-popup">Erreur ...</div>
        <img :src="avatarSrc" alt="Avatar" class="avatar" />
      </el-tooltip>
    </el-header>
    <el-scrollbar wrap-style="overflow-x: hidden;">
      <el-main>
        <nuxt />
      </el-main>
    </el-scrollbar>
    <el-footer height="80px">
      © {{ new Date().getFullYear() }} flapili.fr
      <div style="margin-top: 10px">
        <a
          href="https://cours.cocadmin.com/"
          target="_blank"
          rel="nofollow noopener"
        >
          <img src="~/assets/img/icon.png" class="footer-link" />
        </a>
        <a
          href="https://github.com/flapili/cocaweb"
          target="_blank"
          style="color: inherit"
          rel="nofollow noopener"
        >
          <font-awesome-icon :icon="['fab', 'github']" size="2x" />
        </a>
        <a href="https://flapili.fr/" target="_blank" rel="nofollow noopener">
          <img src="~/assets/img/flapili.webp" class="footer-link" />
        </a>
      </div>
    </el-footer>
  </el-container>
</template>

<script>
export default {
  middleware: "authenticated",

  data() {
    return {
      me: {},
    };
  },
  async fetch() {
    this.me = await this.$api.$get("/discord_Oauth2/@me", {
      params: { guild_id: "532970830246707244" },
    });
  },

  methods: {
    async disconnect() {
      await this.$api.delete("/discord_Oauth2/disconnect");
      this.$router.go();
    },
  },

  computed: {
    avatarSrc() {
      if (this.me && this.me.id) {
        return this.$common.get_avatar(
          this.me.id,
          this.me.discriminator,
          this.me.avatar
        );
      } else {
        return "https://cdn.discordapp.com/embed/avatars/0.png"; // default avatar
      }
    },
  },
};
</script>

<style scoped>
.el-header {
  background-color: #2c2f33;
  display: flex;
}

.header-link {
  margin-top: 5px;
}

.header-link:nth-child(n + 2) {
  margin-left: 20px;
}

.header-link > svg {
  height: 50px;
  width: 50px;
}

.avatar {
  height: 40px;
  width: 40px;
  border-radius: 20px;
  margin-top: 10px;
  margin-left: auto;
}

.avatar-popup {
  font-size: 1.25rem;
  text-align: right;
}

.el-scrollbar {
  height: calc(100vh - 140px);
}

.el-main {
  background-color: #7289da;
  min-height: calc(100vh - 140px);
}

.el-footer {
  background-color: #23272a;
  text-align: center;
  color: white;
  padding-top: 10px;
}

.footer-link {
  height: 32px;
  width: 32px;
  border-radius: 50%;
  margin-left: 15px;
  margin-right: 15px;
}
</style>

<style>
.el-scrollbar__thumb {
  background-color: #23272a;
}

.el-scrollbar__thumb:hover {
  background-color: #000000;
}
</style>