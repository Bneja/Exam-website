const signupPage = {
    template:/*html*/`
    <form class="login-signup" v-on:submit.prevent="trySignup">
        <fieldset id="signup">
            <legend>Signup</legend>
            <p class="error"  v-if="errorMessage">{{errorMessage}}</p>
            <p class="error"  v-if="errorUsername">{{errorUsername}}</p>
            <div class="input-container">
                <label for="reg-user">Username</label>
                <input type="text" v-model="inpUsername" id="reg-user" autocomplete="username">
            </div>
            <p class="error"  v-if="errorPassword">{{errorPassword}}</p>
            <div class="input-container">
                <label for="reg-password">Password</label>
                <input type="password" v-model="inpPassword" id="reg-password" autocomplete="new-password">
            </div>
            <div class="input-container">
                <label for="conf-reg-password">Confirm password</label>
                <input type="password" v-model="inpConfPassword" id="conf-reg-password" autocomplete="new-password">
            </div>
            <div class="input-container">
                <input type="submit" class="submit" value="Signup">
            </div>
        </fieldset>
    </form>
    `,
    emits: ["login", "updateCart"],
    data: function () {
        return {
            inpUsername: "",
            inpPassword: "",
            inpConfPassword: "",
            errorMessage: "",
            errorPassword: "",
            errorUsername: ""
        }
    },
    methods: {
        checkPassword: function (password) {
            // The regular expression matches passwords that:
            // - Have a minimum length of 5 characters
            // - Contain at least one letter (uppercase or lowercase)
            // - Only consist of letters (uppercase or lowercase) and digits (0-9)
            const regex = /^(?=.*[A-Za-z])[A-Za-z0-9]{5,}$/
            if (!regex.test(password)) {
                this.errorPassword = "Password must have at least 5 characters, one letter and only contain letters and numbers"
                setTimeout(()=>this.errorPassword="",5000)
                return false
            }
            this.errorPassword = ""
            return true
        },
        checkUsername: function (username) {
            // The regular expression matches usernames that:
            // - Have a minimum length of 3 characters and a maximum length of 10 characters
            // - Consist of only letters (uppercase or lowercase) and digits (0-9)
            const regex = /^[a-zA-Z0-9]{3,10}$/
            if (!regex.test(username)) {
                this.errorUsername = "Username must be between 3-10 characters and only contain letters and numbers"
                setTimeout(()=>this.errorUsername="",5000)
                return false
            }
            this.errorUsername = ""
            return true
        }
        ,
        trySignup: async function () {
            if (this.checkUsername(this.inpUsername) &&
                this.checkPassword(this.inpPassword) &&
                this.inpConfPassword === this.inpPassword) {
                let response = await fetch("/signup", {
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
                    this.$emit('updateCart')
                    this.$router.push('/')
                } else {
                    let err = await response.json()
                    this.errorMessage = err.message
                }
            } else if (this.checkUsername(this.inpUsername) &&
                this.checkPassword(this.inpPassword) &&
                this.inpConfPassword !== this.inpPassword) {
                this.errorMessage = "The password does not match the confirmation"
            }
            setTimeout(()=>this.errorMessage="",5000)
        }
    }
}