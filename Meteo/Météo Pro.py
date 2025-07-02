import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
import time

# Constantes
VILLES_FRANCAISES = [
    # Grandes métropoles
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", 
    "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Grenoble",
    "Dijon", "Angers", "Nîmes", "Villeurbanne", "Aix-en-Provence", "Le Mans", "Brest", "Tours", 
    "Amiens", "Limoges", "Annecy", "Perpignan", "Metz", "Besançon", "Orléans", "Rouen", "Mulhouse",
    "Caen", "Nancy", "Saint-Denis", "Argenteuil", "Montreuil", "Roubaix", "Tourcoing", "Nanterre", 
    "Avignon", "Créteil", "Poitiers", "Clermont-Ferrand", "Pau", "La Rochelle", "Calais", "Cannes",
    "Colmar", "Saint-Nazaire", "Saint-Quentin", "Valence", "Chambéry", "Vannes", "Saint-Malo", 
    "Troyes", "Béziers", "Montauban", "Chalon-sur-Saône", "Cholet", "Évreux", "Alès", "Bourges",
    "La Roche-sur-Yon", "Charleville-Mézières", "Beauvais", "Mâcon", "Blois", "Nevers", "Auxerre",
    
    # Villes moyennes importantes
    "Bayonne", "Lorient", "Bourg-en-Bresse", "Laval", "Tarbes", "Épinal", "Montluçon", "Châlons-en-Champagne",
    "Angoulême", "Saint-Brieuc", "Niort", "Châteauroux", "Périgueux", "Agen", "Castres", "Arras",
    "Montbéliard", "Ajaccio", "Bastia", "Carcassonne", "Albi", "Rodez", "Auch", "Cahors", "Mende",
    "Foix", "Privas", "Gap", "Digne-les-Bains", "Draguignan", "Grasse", "Hyères", "Fréjus",
    "Saint-Raphaël", "Antibes", "Menton", "Villeneuve-sur-Lot", "Bergerac", "Brive-la-Gaillarde",
    "Tulle", "Guéret", "Aurillac", "Le Puy-en-Velay", "Moulins", "Vichy", "Roanne", "Annemasse",
    "Thonon-les-Bains", "Albertville", "Bourg-Saint-Maurice", "Chamonix-Mont-Blanc", "Megève",
    
    # Banlieues parisiennes importantes
    "Boulogne-Billancourt", "Colombes", "Asnières-sur-Seine", "Versailles", "Courbevoie", 
    "Vitry-sur-Seine", "Aubervilliers", "Saint-Maur-des-Fossés", "Drancy", "Issy-les-Moulineaux", 
    "Noisy-le-Grand", "Levallois-Perret", "Cergy", "Saint-Ouen", "Ivry-sur-Seine", 
    "Neuilly-sur-Seine", "Sarcelles", "Le Blanc-Mesnil", "Clichy", "Pantin", "Bobigny",
    "Bondy", "Noisy-le-Sec", "Rosny-sous-Bois", "Fontenay-sous-Bois", "Vincennes", "Nogent-sur-Marne",
    "Champigny-sur-Marne", "Maisons-Alfort", "Alfortville", "Choisy-le-Roi", "Thiais", "Cachan",
    "Arcueil", "Gentilly", "Le Kremlin-Bicêtre", "Villejuif", "L'Haÿ-les-Roses", "Fresnes",
    "Rungis", "Chevilly-Larue", "Antony", "Châtenay-Malabry", "Le Plessis-Robinson", "Clamart",
    "Meudon", "Sèvres", "Saint-Cloud", "Rueil-Malmaison", "Nanterre", "Puteaux", "Suresnes",
    "Bois-Colombes", "La Garenne-Colombes", "Gennevilliers", "Villeneuve-la-Garenne", "Épinay-sur-Seine",
    "Saint-Denis", "Pierrefitte-sur-Seine", "Stains", "La Courneuve", "Dugny", "Le Bourget",
    "Drancy", "Bobigny", "Pantin", "Les Lilas", "Le Pré-Saint-Gervais", "Bagnolet", "Montreuil",
    "Vincennes", "Fontenay-sous-Bois", "Nogent-sur-Marne", "Joinville-le-Pont", "Saint-Maurice",
    "Charenton-le-Pont", "Maisons-Alfort", "Créteil", "Bonneuil-sur-Marne", "Sucy-en-Brie",
    "Boissy-Saint-Léger", "Limeil-Brévannes", "Valenton", "Villeneuve-Saint-Georges", "Villeneuve-le-Roi",
    "Ablon-sur-Seine", "Vitry-sur-Seine", "Chevilly-Larue", "L'Haÿ-les-Roses", "Cachan", "Arcueil",
    
    # DOM-TOM principales villes
    "Fort-de-France", "Le Lamentin", "Schoelcher", "Sainte-Marie", "Rivière-Pilote", "Le Robert",
    "Saint-Pierre", "Le François", "Sainte-Anne", "Les Trois-Îlets", "Ducos", "Le Vauclin",
    "Pointe-à-Pitre", "Les Abymes", "Baie-Mahault", "Le Gosier", "Sainte-Anne", "Saint-François",
    "Petit-Bourg", "Lamentin", "Capesterre-Belle-Eau", "Basse-Terre", "Gourbeyre", "Trois-Rivières",
    "Saint-Denis", "Saint-Paul", "Saint-Pierre", "Le Tampon", "Saint-Louis", "Saint-André",
    "Saint-Joseph", "Saint-Leu", "La Possession", "Le Port", "Sainte-Marie", "Sainte-Suzanne",
    "Saint-Benoît", "Entre-Deux", "Les Avirons", "Étang-Salé", "Petite-Île", "Saint-Philippe",
    "Cayenne", "Kourou", "Saint-Laurent-du-Maroni", "Matoury", "Rémire-Montjoly", "Macouria",
    "Mana", "Sinnamary", "Iracoubo", "Saint-Georges", "Régina", "Roura", "Montsinéry-Tonnegrande",
    "Mamoudzou", "Dzaoudzi", "Pamandzi", "Dembeni", "Bandrele", "Kani-Kéli", "Bouéni", "Chirongui",
    "Sada", "Ouangani", "Chiconi", "Tsingoni", "M'Tsangamouji", "Acoua", "Mtsamboro", "Bandraboua",
    "Koungou", "Passamaïnty", 
    
    # Villes historiques et touristiques
    "Carcassonne", "Lourdes", "Mont-Saint-Michel", "Fougères", "Rocamadour", "Sarlat-la-Canéda", "Collioure",
    "Honfleur", "Deauville", "Trouville-sur-Mer", "Cabourg", "Étretat", "Fécamp", "Dieppe",
    "Saint-Malo", "Dinard", "Quimper", "Concarneau", "Pont-Aven", "Carnac", "La Baule-Escoublac",
    "Les Sables-d'Olonne", "Royan", "Arcachon", "Biarritz", "Saint-Jean-de-Luz", "Hendaye",
    "Luchon", "Cauterets", "Lourdes", "Pau", "Oloron-Sainte-Marie", "Orthez", "Dax", "Hossegor",
    "Capbreton", "Mimizan", "Biscarrosse", "Marmande", "Nérac", "Condom", "Lectoure", "Fleurance",
    "L'Isle-Jourdain", "Auch", "Mirande", "Marciac", "Vic-Fezensac", "Eauze", "Nogaro",
    "Avignon", "Orange", "Carpentras", "Vaison-la-Romaine", "Apt", "Cavaillon", "Pertuis",
    "Manosque", "Sisteron", "Forcalquier", "Digne-les-Bains", "Castellane", "Moustiers-Sainte-Marie",
    "Riez", "Gréoux-les-Bains", "Valensole", "Banon", "Simiane-la-Rotonde", "Sault",
    "Nice", "Cannes", "Antibes", "Grasse", "Vence", "Saint-Paul-de-Vence", "Cagnes-sur-Mer",
    "Villeneuve-Loubet", "Biot", "Mougins", "Le Cannet", "Vallauris", "Juan-les-Pins", "Golfe-Juan",
    "Saint-Raphaël", "Fréjus", "Sainte-Maxime", "Saint-Tropez", "Cogolin", "Grimaud", "La Garde-Freinet",
    "Le Lavandou", "Bormes-les-Mimosas", "Hyères", "La Londe-les-Maures", "Pierrefeu-du-Var",
    "Collobrières", "La Garde", "Toulon", "Six-Fours-les-Plages", "Sanary-sur-Mer", "Bandol",
    "Saint-Cyr-sur-Mer", "La Ciotat", "Cassis", "Aubagne", "Marseille", "Martigues", "Istres",
    "Salon-de-Provence", "Aix-en-Provence", "Gardanne", "Vitrolles", "Marignane", "Miramas",
    "Port-de-Bouc", "Fos-sur-Mer", "Port-Saint-Louis-du-Rhône", "Arles", "Saintes-Maries-de-la-Mer",
    "Aigues-Mortes", "Le Grau-du-Roi", "La Grande-Motte", "Palavas-les-Flots", "Carnon",
    "Mauguio", "Lattes", "Pérols", "Montpellier", "Castelnau-le-Lez", "Clapiers", "Jacou",
    "Saint-Clément-de-Rivière", "Grabels", "Juvignac", "Lavérune", "Pignan", "Fabrègues",
    "Villeneuve-lès-Maguelone", "Frontignan", "Vic-la-Gardiole", "Mireval", "Villeveyrac",
    "Poussan", "Bouzigues", "Loupian", "Mèze", "Marseillan", "Agde", "Vias", "Portiragnes",
    "Sérignan", "Valras-Plage", "Vendres", "Lespignan", "Fleury", "Coursan", "Sigean",
    "Port-la-Nouvelle", "Leucate", "Fitou", "Tuchan", "Paziols", "Durban-Corbières", "Albas",
    "Lézignan-Corbières", "Narbonne", "Cuxac-d'Aude", "Moussan", "Sallèles-d'Aude", "Ginestas",
    "Marcorignan", "Paraza", "Roubia", "Capendu", "Trèbes", "Carcassonne", "Pennautier",
    "Villemoustaussou", "Villalier", "Conques-sur-Orbiel", "Lastours", "Salsigne", "Villanière"
]

VILLES_INTERNATIONALES = [
    # Capitales et grandes métropoles mondiales
    "London", "Paris", "Berlin", "Madrid", "Rome", "Moscow", "Amsterdam", "Brussels", "Vienna",
    "Zurich", "Stockholm", "Oslo", "Helsinki", "Copenhagen", "Dublin", "Warsaw", "Prague", 
    "Budapest", "Bucharest", "Athens", "Lisbon",
    
    # Amérique du Nord
    "New York", "Los Angeles", "Chicago", "Toronto", "Montreal", "Vancouver", "Washington", 
    "Boston", "San Francisco", "Seattle", "Miami", "Las Vegas", "Philadelphia", "Detroit",
    
    # Asie
    "Tokyo", "Beijing", "Shanghai", "Seoul", "Singapore", "Hong Kong", "Bangkok", "Mumbai", 
    "Delhi", "Jakarta", "Kuala Lumpur", "Manila", "Taipei", "Osaka", "Kyoto",
    
    # Océanie
    "Sydney", "Melbourne", "Brisbane", "Perth", "Auckland", "Wellington",
    
    # Moyen-Orient
    "Dubai", "Abu Dhabi", "Doha", "Kuwait City", "Riyadh", "Tehran", "Istanbul", "Cairo",
    
    # Amérique du Sud
    "São Paulo", "Rio de Janeiro", "Buenos Aires", "Lima", "Santiago", "Bogotá", "Caracas",
    
    # Afrique
    "Lagos", "Cairo", "Cape Town", "Johannesburg", "Nairobi", "Casablanca", "Tunis", "Algiers"
]

COULEURS = {
    'bg': "#1C1C1E",
    'card': "#2C2C2E", 
    'input': "#232326",
    'text_primary': "#FFFFFF",
    'text_secondary': "#A1A1AA",
    'accent': "#0A84FF",
    'success': "#30D158",
    'warning': "#FFD60A"
}

EMOJIS_METEO = {
    0: '☀️',     # Ciel dégagé
    1: '🌤️',     # Principalement dégagé  
    2: '⛅',     # Partiellement nuageux
    3: '☁️',     # Couvert
    45: '🌫️', 48: '🌫️',   # Brouillard
    51: '🌦️', 53: '🌧️', 55: '🌧️',   # Bruine
    61: '🌧️', 63: '🌧️', 65: '🌧️',   # Pluie
    71: '❄️', 73: '❄️', 75: '❄️',   # Neige
    80: '🌦️', 81: '🌧️', 82: '⛈️',   # Averses pluie
    85: '🌨️', 86: '🌨️',   # Averses neige
    95: '⛈️', 96: '⛈️', 99: '⛈️'   # Orages
}

class AppMeteo:
    def __init__(self, root):
        self.root = root
        self.villes = VILLES_FRANCAISES + VILLES_INTERNATIONALES
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        
        # Cache simple
        self.cache_data = {}
        self.cache_time = {}
        self.cache_duration = 600  # 10 minutes
        
        self._configurer_fenetre()
        self.ville_auto = self._detecter_ville_auto()
        self._creer_interface()

    def _configurer_fenetre(self):
        """Configure la fenêtre principale"""
        self.root.title("🌤️ Météo Pro")
        self.root.geometry("650x950")
        self.root.configure(bg=COULEURS['bg'])
        self.root.resizable(True, True)

    def _detecter_ville_auto(self):
        """Détecte automatiquement la ville de l'utilisateur"""
        print("🔍 Détection automatique de votre localisation...")
        
        try:
            response = requests.get('https://ipinfo.io/json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                ville = data.get('city', 'Paris')
                print(f"✅ Localisation détectée: {ville} ({data.get('country', 'FR')})")
                return ville
        except Exception as e:
            print(f"❌ Détection automatique échouée: {e}")
        
        print("⚠️ Utilisation de Paris par défaut")
        return "Paris"

    def _creer_interface(self):
        """Crée l'interface utilisateur"""
        self.var_ville = tk.StringVar()
        
        # Container principal
        main_container = tk.Frame(self.root, bg=COULEURS['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Conteneur pour le contenu principal
        content_container = tk.Frame(main_container, bg=COULEURS['bg'])
        content_container.pack(fill=tk.BOTH, expand=True)
        
        self._creer_header(content_container)
        self._creer_recherche(content_container)
        
        # Frame pour les résultats météo
        self.frame_resultats = tk.Frame(content_container, bg=COULEURS['card'])
        self.frame_resultats.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        
        # Crédit développeur
        self._creer_credit_dev(main_container)

    def _creer_header(self, parent):
        """Crée l'en-tête de l'application"""
        header_frame = tk.Frame(parent, bg=COULEURS['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(header_frame, text="🌤️ Météo Pro", font=("SF Pro Display", 32, "bold"),
                bg=COULEURS['bg'], fg=COULEURS['text_primary']).pack()
        
        tk.Label(header_frame, text="Station météorologique moderne", font=("SF Pro Text", 16),
                bg=COULEURS['bg'], fg=COULEURS['text_secondary']).pack(pady=(5, 0))
    
    def _creer_recherche(self, parent):
        """Crée la section de recherche"""
        search_card = tk.Frame(parent, bg=COULEURS['card'], relief=tk.FLAT, bd=0)
        search_card.pack(fill=tk.X, pady=(0, 20))
        
        search_inner = tk.Frame(search_card, bg=COULEURS['card'])
        search_inner.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(search_inner, text="Rechercher une ville", font=("SF Pro Text", 14),
                bg=COULEURS['card'], fg=COULEURS['text_primary']).pack(anchor=tk.W, pady=(0, 10))
        
        # Input et bouton
        input_frame = tk.Frame(search_inner, bg=COULEURS['card'])
        input_frame.pack(fill=tk.X)
        
        self._creer_champ_saisie(input_frame)
        self._creer_bouton_recherche(input_frame)
        self._creer_suggestions(search_inner)

    def _creer_champ_saisie(self, parent):
        """Crée le champ de saisie"""
        self.entry_ville = tk.Entry(
            parent, textvariable=self.var_ville, font=("SF Pro Text", 16),
            bg=COULEURS['input'], fg=COULEURS['text_primary'], insertbackground=COULEURS['text_primary'],
            relief=tk.FLAT, bd=0, highlightthickness=1, highlightcolor=COULEURS['accent'],
            highlightbackground=COULEURS['input']
        )
        self.entry_ville.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, ipadx=15)
        self.entry_ville.bind("<Return>", lambda e: self.rechercher_meteo())
        self.entry_ville.bind("<FocusOut>", lambda e: self.listbox_suggestions.pack_forget())

    def _creer_bouton_recherche(self, parent):
        """Crée le bouton de recherche"""
        tk.Button(
            parent, text="🔍", font=("SF Pro Text", 16, "bold"),
            bg=COULEURS['accent'], fg="white", activebackground="#005BB5",
            relief=tk.FLAT, bd=0, command=self.rechercher_meteo,
            cursor="hand2", width=3, height=1
        ).pack(side=tk.RIGHT, padx=(8, 0))

    def _creer_suggestions(self, parent):
        """Crée la liste des suggestions"""
        self.listbox_suggestions = tk.Listbox(
            parent, font=("SF Pro Text", 12), bg=COULEURS['input'], fg=COULEURS['text_secondary'],
            bd=0, highlightthickness=0, relief=tk.FLAT, selectbackground=COULEURS['accent'],
            selectforeground="white"
        )
        self.listbox_suggestions.pack_forget()
        
        # Bindings pour autocomplétion
        self.var_ville.trace_add('write', self._update_suggestions)
        self.entry_ville.bind('<Down>', self._select_suggestion)
        self.listbox_suggestions.bind('<ButtonRelease-1>', self._choose_suggestion)
        self.listbox_suggestions.bind('<Return>', self._choose_suggestion)
    
    def _update_suggestions(self, *args):
        """Met à jour les suggestions d'autocomplétion"""
        value = self.var_ville.get().lower()
        if value and len(value) >= 2:
            matches = [v for v in self.villes if v.lower().startswith(value)][:6]
            if matches:
                self.listbox_suggestions.delete(0, tk.END)
                for ville in matches:
                    self.listbox_suggestions.insert(tk.END, ville)
                self.listbox_suggestions.pack(fill=tk.X, pady=(5, 0))
            else:
                self.listbox_suggestions.pack_forget()
        else:
            self.listbox_suggestions.pack_forget()

    def _select_suggestion(self, event):
        """Sélectionne la première suggestion avec la flèche bas"""
        if self.listbox_suggestions.size() > 0:
            self.listbox_suggestions.focus_set()
            self.listbox_suggestions.selection_clear(0, tk.END)
            self.listbox_suggestions.selection_set(0)
            return 'break'

    def _choose_suggestion(self, event):
        """Choisit une suggestion et lance la recherche"""
        selection = self.listbox_suggestions.curselection()
        if selection:
            ville = self.listbox_suggestions.get(selection[0])
            self.var_ville.set(ville)
            self.listbox_suggestions.pack_forget()
            self.entry_ville.icursor(tk.END)
            self.entry_ville.focus_set()
    
    def rechercher_meteo(self):
        """Lance la recherche météo"""
        self.listbox_suggestions.pack_forget()
        self._obtenir_meteo()
    
    def _obtenir_meteo(self):
        """Récupère les données météo"""
        ville = self.entry_ville.get().strip() or self.ville_auto
        
        if not ville:
            messagebox.showwarning("Attention", "Veuillez entrer le nom d'une ville")
            return

        print(f"Recherche de la météo pour: {ville}")
        
        # Vérifier le cache
        if self._est_dans_cache(ville):
            data = self.cache_data[ville]
            print("✅ Données récupérées depuis le cache")
        else:
            data = self._get_weather_data(ville)
            if data:
                self.cache_data[ville] = data
                self.cache_time[ville] = self._current_time()
                print("✅ Données récupérées depuis l'API")
            else:
                messagebox.showerror("Erreur", f"Ville '{ville}' non trouvée")
                return
            
        self._afficher_meteo(data, ville)
    
    def _est_dans_cache(self, ville):
        """Vérifie si les données sont dans le cache et valides"""
        if ville in self.cache_data:
            age_cache = self._current_time() - self.cache_time[ville]
            if age_cache < self.cache_duration:
                return True
            else:
                print("⏳ Cache expiré, nouvelle requête nécessaire")
                return False
        return False
    
    def _current_time(self):
        """Renvoie l'heure actuelle en secondes"""
        return int(time.time())
    
    def _get_weather_data(self, city):
        """Récupère les données météo depuis l'API Open-Meteo"""
        lat, lon = self._get_coordinates(city)
        
        if lat is None or lon is None:
            return None
        
        url = (f"{self.base_url}?"
               f"latitude={lat}&longitude={lon}&"
               f"current=temperature_2m,relative_humidity_2m,apparent_temperature,"
               f"is_day,precipitation,weather_code,cloud_cover,pressure_msl,"
               f"wind_speed_10m,wind_direction_10m,wind_gusts_10m&"
               f"daily=weather_code,temperature_2m_max,temperature_2m_min,"
               f"sunrise,sunset,uv_index_max,precipitation_sum,"
               f"wind_speed_10m_max&"
               f"timezone=auto")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"🌐 Nouvelles données récupérées pour {city}")
                return data
            else:
                print(f"Erreur API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Erreur lors de la récupération des données météo: {e}")
            return None
            
    def _get_coordinates(self, city):
        """Convertit le nom d'une ville en coordonnées"""
        if not city:
            return None, None
            
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        
        try:
            headers = {'User-Agent': 'Meteo App/1.0'}
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
            else:
                return None, None
        except Exception as e:
            print(f"Erreur lors de la géolocalisation: {e}")
            return None, None
    
    def _afficher_meteo(self, data, ville):
        """Affiche les données météo"""
        # Effacer les résultats précédents
        for widget in self.frame_resultats.winfo_children():
            widget.destroy()
        
        try:
            current = data.get('current', {})
            daily = data.get('daily', {})
            
            # Données actuelles
            temperature = current.get('temperature_2m', 0)
            humidity = current.get('relative_humidity_2m', 0)
            apparent_temp = current.get('apparent_temperature', 0)
            wind_speed = current.get('wind_speed_10m', 0)
            wind_direction = current.get('wind_direction_10m', 0)
            wind_gusts = current.get('wind_gusts_10m', 0)
            weather_code = current.get('weather_code', 0)
            pressure = current.get('pressure_msl', 0)
            cloud_cover = current.get('cloud_cover', 0)
            is_day = current.get('is_day', 1)
            
            # Données journalières
            if daily and daily.get('time'):
                temp_max = daily.get('temperature_2m_max', [0])[0]
                temp_min = daily.get('temperature_2m_min', [0])[0]
                sunrise = daily.get('sunrise', [''])[0].split('T')[1][:5] if daily.get('sunrise') else 'N/A'
                sunset = daily.get('sunset', [''])[0].split('T')[1][:5] if daily.get('sunset') else 'N/A'
                uv_index = daily.get('uv_index_max', [0])[0]
            else:
                temp_max = temp_min = uv_index = 0
                sunrise = sunset = 'N/A'
            
            emoji_meteo = self._obtenir_emoji_meteo(weather_code)
            description = self._get_weather_description(weather_code)
            wind_direction_text = self._get_wind_direction(wind_direction)
            
            # === TITRE PRINCIPAL ===
            header_frame = tk.Frame(self.frame_resultats, bg=COULEURS['card'])
            header_frame.pack(pady=20, fill=tk.X)
            
            tk.Label(header_frame, text=f"📍 {ville}", font=("SF Pro Display", 24, "bold"),
                    bg=COULEURS['card'], fg=COULEURS['text_primary']).pack()
            
            # === TEMPÉRATURE PRINCIPALE ===
            temp_frame = tk.Frame(self.frame_resultats, bg=COULEURS['card'])
            temp_frame.pack(pady=20)
            
            tk.Label(temp_frame, text=emoji_meteo, font=("Arial", 60), bg=COULEURS['card']).pack(side=tk.LEFT)
            tk.Label(temp_frame, text=f"{temperature:.1f}°C", font=("SF Pro Display", 50, "bold"),
                    bg=COULEURS['card'], fg=COULEURS['accent']).pack(side=tk.LEFT, padx=20)
            
            # === DESCRIPTION ET RESSENTI ===
            tk.Label(self.frame_resultats, text=description, font=("SF Pro Text", 18),
                    bg=COULEURS['card'], fg=COULEURS['text_secondary']).pack(pady=5)
            tk.Label(self.frame_resultats, text=f"Ressenti: {apparent_temp:.1f}°C", font=("SF Pro Text", 16),
                    bg=COULEURS['card'], fg=COULEURS['text_secondary']).pack(pady=5)
            
            # === TEMPÉRATURES MIN/MAX ===
            minmax_frame = tk.Frame(self.frame_resultats, bg=COULEURS['card'])
            minmax_frame.pack(pady=15)
            self._create_label(minmax_frame, f"🔼 Max: {temp_max:.1f}°C", 14, 'warning').pack(side=tk.LEFT, padx=15)
            self._create_label(minmax_frame, f"🔽 Min: {temp_min:.1f}°C", 14, 'accent').pack(side=tk.LEFT, padx=15)
            
            # === SECTIONS DÉTAILLÉES ===
            # Vent
            wind_details = self._create_section(self.frame_resultats, "🌬️ VENT")
            self._create_label(wind_details, f"Vitesse: {wind_speed:.1f} km/h", color='text_secondary').pack(side=tk.LEFT, padx=10)
            self._create_label(wind_details, f"Rafales: {wind_gusts:.1f} km/h", color='text_secondary').pack(side=tk.LEFT, padx=10)
            self._create_label(wind_details, f"Direction: {wind_direction_text}", color='text_secondary').pack(side=tk.LEFT, padx=10)
            
            # Atmosphère
            atmo_details = self._create_section(self.frame_resultats, "🌍 ATMOSPHÈRE")
            self._create_label(atmo_details, f"💧 Humidité: {humidity:.0f}%").pack(side=tk.LEFT, padx=15)
            self._create_label(atmo_details, f"📊 Pression: {pressure:.0f} hPa").pack(side=tk.LEFT, padx=15)
            self._create_label(atmo_details, f"☁️ Nuages: {cloud_cover:.0f}%").pack(side=tk.LEFT, padx=15)
            
            # Soleil
            sun_details = self._create_section(self.frame_resultats, "☀️ SOLEIL")
            self._create_label(sun_details, f"🌅 Lever: {sunrise}", color='text_secondary').pack(side=tk.LEFT, padx=15)
            self._create_label(sun_details, f"🌇 Coucher: {sunset}", color='text_secondary').pack(side=tk.LEFT, padx=15)
            tk.Label(sun_details, text=f"🔆 UV Index: {uv_index:.1f}", font=("SF Pro Text", 12),
                    bg=COULEURS['card'], fg=self._get_uv_color(uv_index)).pack(side=tk.LEFT, padx=15)
            
            # === BOUTON ACTUALISER ===
            buttons_frame = tk.Frame(self.frame_resultats, bg=COULEURS['card'])
            buttons_frame.pack(pady=30)
            
            tk.Button(buttons_frame, text="🔄 Actualiser", font=("SF Pro Text", 14, "bold"),
                    bg=COULEURS['accent'], fg="white", activebackground="#0051A8",
                    relief=tk.FLAT, bd=0, command=self._obtenir_meteo,
                    cursor="hand2", pady=10, padx=20).pack()
            
            # === STATUT ===
            status_text = f"🌞 Jour" if is_day else f"🌙 Nuit"
            tk.Label(self.frame_resultats, text=status_text, font=("SF Pro Text", 12),
                    bg=COULEURS['card'], fg=COULEURS['text_secondary']).pack(pady=10)
            
        except Exception as e:
            print(f"Erreur lors de l'affichage des données météo: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du traitement des données: {e}")

    def _obtenir_emoji_meteo(self, weather_code):
        """Retourne un emoji basé sur le code météo"""
        return EMOJIS_METEO.get(weather_code, '🌤️')
        
    def _get_weather_description(self, code):
        """Retourne une description basée sur le code météo"""
        descriptions = {
            0: "Ciel dégagé",
            1: "Principalement dégagé",
            2: "Partiellement nuageux",
            3: "Couvert",
            45: "Brouillard",
            48: "Brouillard givrant",
            51: "Bruine légère",
            53: "Bruine modérée",
            55: "Bruine dense",
            61: "Pluie légère",
            63: "Pluie modérée",
            65: "Pluie forte",
            71: "Chute de neige légère",
            73: "Chute de neige modérée",
            75: "Chute de neige forte",
            80: "Averses de pluie légères",
            81: "Averses de pluie modérées",
            82: "Averses de pluie violentes",
            85: "Averses de neige légères",
            86: "Averses de neige fortes",
            95: "Orage",
            96: "Orage avec grêle légère",
            99: "Orage avec grêle forte"
        }
        return descriptions.get(code, "Conditions météo inconnues")
    
    def _get_wind_direction(self, direction):
        """Convertit la direction du vent en degrés vers du texte"""
        if direction is None:
            return "N/A"
        
        directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"
        ]
        index = round(direction / 22.5) % 16
        return f"{directions[index]} ({direction:.0f}°)"
    
    def _get_uv_color(self, uv_index):
        """Retourne la couleur appropriée selon l'index UV"""
        if uv_index <= 2:
            return COULEURS['success']  # Vert - Faible
        elif uv_index <= 5:
            return COULEURS['warning']  # Jaune - Modéré
        elif uv_index <= 7:
            return "#FF9500"  # Orange - Élevé
        elif uv_index <= 10:
            return "#FF3B30"  # Rouge - Très élevé
        else:
            return "#AF52DE"  # Violet - Extrême
    
    def _creer_credit_dev(self, parent):
        """Crée la section crédit développeur"""
        credit_frame = tk.Frame(parent, bg=COULEURS['input'], height=50, relief=tk.FLAT, bd=1)
        credit_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))
        credit_frame.pack_propagate(False)
        
        # Container centré pour le contenu
        content_frame = tk.Frame(credit_frame, bg=COULEURS['input'])
        content_frame.pack(expand=True)
        
        tk.Label(content_frame, text="Développé par solvyrth • ", font=("SF Pro Text", 11),
                bg=COULEURS['input'], fg=COULEURS['text_primary']).pack(side=tk.LEFT, pady=10)
        
        github_label = tk.Label(content_frame, text="GitHub", font=("SF Pro Text", 11, "underline"),
                               bg=COULEURS['input'], fg=COULEURS['accent'], cursor="hand2")
        github_label.pack(side=tk.LEFT, pady=10)
        github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/solvyrth"))

    def _create_label(self, parent, text, font_size=12, color='text_primary', **pack_options):
        """Helper pour créer des labels avec style uniforme"""
        return tk.Label(parent, text=text, font=("SF Pro Text", font_size),
                       bg=COULEURS['card'], fg=COULEURS[color], **pack_options)

    def _create_section(self, parent, title, pady=20):
        """Helper pour créer une section avec titre"""
        section_frame = tk.Frame(parent, bg=COULEURS['card'])
        section_frame.pack(pady=pady, fill=tk.X)
        
        tk.Label(section_frame, text=title, font=("SF Pro Text", 14, "bold"),
                bg=COULEURS['card'], fg=COULEURS['text_primary']).pack()
        
        details_frame = tk.Frame(section_frame, bg=COULEURS['card'])
        details_frame.pack(pady=10)
        return details_frame


if __name__ == "__main__":
    root = tk.Tk()
    app = AppMeteo(root)
    root.mainloop()
