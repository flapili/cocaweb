export default {
    // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
    ssr: false,

    // Target: https://go.nuxtjs.dev/config-target
    target: 'server',

    server: {
        host: "0.0.0.0",
    },

    vue: {
        config: {
            // productionTip: true,
            devtools: true,
            silent: false,
        }
    },

    generate: {
        dir: "../dist",
    },
    // Global page headers: https://go.nuxtjs.dev/config-head
    head: {
        title: 'CocaWeb by flapili',
        meta: [
            { charset: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            { hid: 'description', name: 'description', content: '' }
        ],
        link: [
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
        ]
    },

    // Global CSS: https://go.nuxtjs.dev/config-css
    css: [
        "~/assets/css/style.css",
        'element-ui/lib/theme-chalk/index.css',
    ],

    // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
    plugins: [
        "@/plugins/api",
        "@/plugins/common-function",
        "@/plugins/element-ui",
    ],

    // Auto import components: https://go.nuxtjs.dev/config-components
    components: true,

    // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
    buildModules: [
        "@nuxtjs/fontawesome",
    ],

    // Modules: https://go.nuxtjs.dev/config-modules
    modules: [
        // https://go.nuxtjs.dev/axios
        '@nuxtjs/axios',
    ],

    // Axios module configuration: https://go.nuxtjs.dev/config-axios
    axios: {},

    fontawesome: {
        icons: {
            solid: [
                "faSignOutAlt",
                "faHome",
                "faChartLine",
            ],
            regular: [],
            light: [],
            duotone: [],
            brands: [
                'faDiscord',
                'faGithub',
            ],
        }
    },


    // Build Configuration: https://go.nuxtjs.dev/config-build
    build: {
        hardSource: true,
        cache: true,
        transpile: [/^element-ui/],
    }
}