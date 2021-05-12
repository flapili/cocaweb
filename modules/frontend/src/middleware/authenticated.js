export default async function({ redirect, $api }) {
    try {
        await $api.get("/discord_Oauth2/@me", { params: { guild_id: "532970830246707244" } })
    } catch (error) {
        if (error.response) {
            redirect(error.response.data.detail.login_url)
        } else {
            console.error(error)
        }
    }
}