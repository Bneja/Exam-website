const loginPage = {
    template:/*html*/`
    <form class="login-signup" v-on:submit.prevent="tryLogin">
        <fieldset id="login">
            <legend>Login</legend>
            <p class="error" id="login-error" v-if="errorMessage">{{errorMessage}}</p>
            <div class="input-container">
                <label for="username">Username</label>
                <input type="text" id="username" v-model="inpUsername" autocomplete="username">
            </div>
            <div class="input-container">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="inpPassword" autocomplete="current-password">
            </div>
            <div class="input-container">
                <input type="submit" class="submit" value="Login">
            </div>
        </fieldset>
    </form>
    `,
    emits: ['login', 'updateCart'],
    data: function () {
        return {
            inpUsername: "",
            inpPassword: "",
            errorMessage: ""
        }
    },
    methods: {
        tryLogin: async function () {
            let response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "username": this.inpUsername, "password": this.inpPassword })
            })

            if (response.status == 200) {
                let user = await response.json()
                this.inpPassword = ""
                this.inpUsername = ""
                this.errorMessage = ""
                this.$emit('login', user)
                this.$emit("updateCart")
                this.$router.push('/')

            } else {
                let err = await response.json()
                this.errorMessage = err.message
                setTimeout(()=>this.errorMessage="",3000)
            }
        }
    },
    watch: {
        closeDialog: function () {
            this.$refs.accDia.close()
        }
    }
}