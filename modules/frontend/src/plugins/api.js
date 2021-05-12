export default function({ $axios }, inject) {
    const api = $axios.create({
        headers: {
            common: {
                'Content-Type': 'application/json'
            }
        }
    });

    api.setBaseURL(`${window.location.origin}/api`)
    inject("api", api)
}