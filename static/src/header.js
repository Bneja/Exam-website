const storeHeader = {
    props: ["user"],
    template:/*html*/`
    <div>
        <router-link to="/">
            <img src="static/src/images/Gulls-and-us.png" id="logo"/>
        </router-link>
    </div>
    <form v-on:submit.prevent="goToSearch" id="search-form">
        <input type="search" placeholder="Search..." id="searchbar" v-model="kword">
        <input type="submit" class="material-symbols-outlined" value="search" id="search-button"/>
    </form>
    <nav>
        <i id="account" class="material-symbols-outlined icon" v-on:click="toggleDia" ref="accIcon">
        account_circle
        </i>
        <div id="acc-dia" ref="accDia">
            <div id="inner-dia">
                <strong v-if="user">{{user.username}}</strong>
                <span v-if="admin">ADMIN</span>
                <button v-if="!user" v-on:click="gotoLogin">Login</button>
                <button v-if="!user" v-on:click="gotoSignup">Signup</button>
                <button v-if="user" v-on:click="logout">Logout</button>
            </div>
        </div>
        <router-link to="/cart" class="material-symbols-outlined icon">
        shopping_cart
        </router-link>
        <router-link to="/" class="material-symbols-outlined icon">
        home
        </router-link>
    </nav>`,
    emits: ['logout'],
    data: function () {
        return {
            kword: this.$route.params.kword
        }
    },
    methods: {
        goToSearch: function () {
            if (this.kword) {
                this.$router.push({ name: "searchPage", params: { kword: this.kword } })
            } else {
                this.$router.push("/")
            }
        },
        toggleDia: function () {
            let diaDisplay=this.$refs.accDia.style.display
            if (diaDisplay==="none" || diaDisplay===""){
                this.$refs.accDia.style.display = "block"
            }else{
                this.$refs.accDia.style.display = "none"
            }
        },
        gotoLogin: function () {
            this.$router.push("/login")
            this.$refs.accDia.style.display = "none"
        },
        gotoSignup: function () {
            this.$router.push("/signup")
            this.$refs.accDia.style.display = "none"
        },
        logout: async function () {
            let response = await fetch("/logout")
            if (response.status == 200) {
                this.$emit('logout')
                this.$router.push('/')
            }
        }
    },
    created: function () {
        document.addEventListener("click", e => {
            const dialogDimensions = this.$refs.accDia.getBoundingClientRect()
            const iconDimensions = this.$refs.accIcon.getBoundingClientRect()
            if (
                (e.clientX < dialogDimensions.left ||
                    e.clientX > dialogDimensions.right ||
                    e.clientY < dialogDimensions.top ||
                    e.clientY > dialogDimensions.bottom)
                &&
                (e.clientX < iconDimensions.left ||
                    e.clientX > iconDimensions.right ||
                    e.clientY < iconDimensions.top ||
                    e.clientY > iconDimensions.bottom)
            ) {
                this.$refs.accDia.style.display = "none"
            }
        })
    },
    watch:{
        $route:{
            handler:function(){
                this.kword=this.$route.params.kword    
            },
            immidiate:true
        },
    },
    computed:{
        admin:function(){
            return (this.user && this.user.role==="admin")
        }
    }
}
