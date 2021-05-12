export default function({}, inject) {
    inject("common", {

        get_avatar(id, discriminator, hash) {
            if (!hash || hash <= 5) {
                const index = discriminator % 5;
                return `https://cdn.discordapp.com/embed/avatars/${index}.png`
            }
            return `https://cdn.discordapp.com/avatars/${id}/${hash}.png`
        }

    })
}