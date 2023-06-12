const cartAside = {
    template:/*html*/`    
    <aside id="side">
    <table>
        <h2>
            <router-link to="/cart">Cart</router-link>
        </h2>
        <tr v-for="item in summaryCart">
            <td><router-link v-bind:to="'/product/'+item.product.id">{{item.product.name}}</router-link></td>
            <td>{{item.product.price*item.quantity}}-&nbsp;kr</td>
            <td>{{item.quantity}}</td>
        </tr>
    </table>
</aside>`,
    props: ["cart"],
    computed:{
        summaryCart:function(){
            if (this.cart){
                let summary=this.cart.slice()
                summary.reverse()
                summary.splice(4)
                return summary
            }
            return []
        }
    }
}