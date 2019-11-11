Vue.config.devtools = true;

Vue.component('state', {
    props: ['status', 'progress'],
    template: `
        <span>
            <span v-if="status == 'startup' || status == 'wait_power_on'">powered off</span>
            <span v-if="status == 'wait_power_off'">running game</span>
            <span v-if="status == 'send_game'">sending game ({{ progress }}% complete)</span>
        </span>
    `,
});

Vue.component('cabinet', {
    props: ['cabinet'],
    template: `
        <div class='cabinet'>
            <h3>{{ cabinet.description }}</h3>
            <dl>
                <dt>Game</dt><dd>{{ cabinet.game }}</dd>
                <dt>Status</dt><dd><state v-bind:status="cabinet.status" v-bind:progress="cabinet.progress"></state></dd>
            </dl>
            <a class="button" v-bind:href="'config/' + cabinet.ip">Configure Cabinet</a>
        </div>
    `,
});

Vue.component('directory', {
    props: ['dir'],
    template: `
        <div class='directory'>
            <div>{{ dir.name }}</div>
            <rom v-for="rom in dir.files" v-bind:rom="rom" v-bind:key="rom"></rom>
        </div>
    `,
});

Vue.component('rom', {
    props: ['rom'],
    template: `
        <div class='rom'>
            {{ rom }}
        </div>
    `,
});

Vue.component('cabinetconfig', {
    data: function() {
        return {
            cabinet: window.cabinet,
            saved: false,
        };
    },
    methods: {
        changed: function() {
            this.saved = false;
        },
        save: function() {
            axios.post('/cabinets/' + this.cabinet.ip, this.cabinet).then(result => {
                if (!result.data.error) {
                    this.cabinet = result.data;
                    this.saved = true;
                }
            });
        },
    },
    template: `
        <div class='cabinet'>
            <dl>
                <dt>IP Address</dt><dd>{{ cabinet.ip }}</dd>
                <dt>Description</dt><dd><input v-model="cabinet.description" @input="changed"/></dd>
                <dt>Region</dt><dd>
                    <select v-model="cabinet.region" @input="changed">
                        <option v-for="region in regions" v-bind:value="region">{{ region }}</option>
                    </select>
                </dd>
                <dt>Target</dt><dd>
                    <select v-model="cabinet.target" @input="changed">
                        <option v-for="target in targets" v-bind:value="target">{{ target }}</option>
                    </select>
                </dd>
                <dt>NetDimm Version</dt><dd>
                    <select v-model="cabinet.version" @input="changed">
                        <option v-for="version in versions" v-bind:value="version">{{ version }}</option>
                    </select>
                </dd>
            </dl>
            <button v-on:click="save">Update Properties</button><span class="indicator" v-if="saved">&check; saved</span>
        </div>
    `,
});

Vue.component('cabinetlist', {
    data: function() {
        return {
            cabinets: window.cabinets,
        };
    },
    methods: {
        refresh: function() {
            axios.get('/cabinets').then(result => {
                if (!result.data.error) {
                    this.cabinets = result.data.cabinets;
                }
            });
        },
    },
    mounted: function() {
        setInterval(function () {
            this.refresh();
        }.bind(this), 1000);
    },
    template: `
        <div>
            <cabinet v-for="cabinet in cabinets" v-bind:cabinet="cabinet" v-bind:key="cabinet.ip"></cabinet>
        </div>
    `,
});

Vue.component('romlist', {
    data: function() {
        return {
            roms: window.roms,
        };
    },
    methods: {
        refresh: function() {
            axios.get('/roms').then(result => {
                if (!result.data.error) {
                    this.roms = result.data.roms;
                }
            });
        },
    },
    mounted: function() {
        setInterval(function () {
            this.refresh();
        }.bind(this), 5000);
    },
    template: `
        <div class='romlist'>
            <h3>Available ROMs</h3>
            <directory v-for="rom in roms" v-bind:dir="rom" v-bind:key="rom"></directory>
        </div>
    `,
});

Vue.component('patchlist', {
    data: function() {
        return {
            patches: window.patches,
        };
    },
    methods: {
        refresh: function() {
            axios.get('/patches').then(result => {
                if (!result.data.error) {
                    this.patches = result.data.patches;
                }
            });
        },
    },
    mounted: function() {
        setInterval(function () {
            this.refresh();
        }.bind(this), 5000);
    },
    template: `
        <div class='patchlist'>
            <h3>Available Patches</h3>
            <directory v-for="patch in patches" v-bind:dir="patch" v-bind:key="patch"></directory>
        </div>
    `,
});
