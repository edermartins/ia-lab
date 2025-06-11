import streamlit as st
from typing import Dict, List
import json
from utils.llm_interface import LLMInterface
import asyncio
from database.models import Database

class StoryEditor:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.db = Database()
        
        # Inicializa as variáveis de estado se não existirem
        if "story" not in st.session_state:
            st.session_state.story = {
                "title": "",
                "genre": "",
                "synopsis": "",
                "chapters": [],
                "timeline": []
            }
        if "current_chapter" not in st.session_state:
            st.session_state.current_chapter = None
        if "chapter_title" not in st.session_state:
            st.session_state.chapter_title = ""
        if "chapter_content" not in st.session_state:
            st.session_state.chapter_content = ""
        if "chapter_suggestions" not in st.session_state:
            st.session_state.chapter_suggestions = ""
        if "timeline_event_title" not in st.session_state:
            st.session_state.timeline_event_title = ""
        if "timeline_event_description" not in st.session_state:
            st.session_state.timeline_event_description = ""
        if "timeline_event_date" not in st.session_state:
            st.session_state.timeline_event_date = ""
        if "story_suggestions" not in st.session_state:
            st.session_state.story_suggestions = ""
    
    def render(self, story_id: str = None):
        """Renderiza o editor de história."""
        st.header("Editor de História")
        
        if not story_id:
            st.info("Preencha os detalhes do seu novo livro abaixo.")
            self._render_story_form()
            return
        
        # Carrega os dados da história
        story = self.db.get_story(story_id)
        if not story:
            st.error("História não encontrada.")
            return
            
        # Mostra os detalhes da história
        st.subheader("Detalhes da História")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Título:** {story['title']}")
            st.write(f"**Gênero:** {story['genre']}")
            st.write(f"**Público-Alvo:** {story['target_audience']}")
            st.write(f"**Tema Principal:** {story['main_theme']}")
        with col2:
            st.write(f"**Estilo Narrativo:** {story['narrative_style']}")
            st.write(f"**Ambientação:** {story['setting']}")
            st.write(f"**Sinopse:** {story['description']}")
        
        st.divider()
        
        # Sidebar para lista de capítulos e eventos
        with st.sidebar:
            st.subheader("Capítulos")
            
            # Botão para criar novo capítulo
            if st.button("Novo Capítulo"):
                st.session_state.chapter_title = ""
                st.session_state.chapter_content = ""
                st.session_state.current_chapter = None
                st.rerun()
            
            # Lista de capítulos
            chapters = self.db.get_story_chapters(story_id)
            if chapters:
                for chapter_id, chapter in chapters.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"📖 {chapter['title']}", key=f"chapter_{chapter_id}"):
                            st.session_state.current_chapter = chapter_id
                            st.session_state.chapter_title = chapter.get("title", "")
                            st.session_state.chapter_content = chapter.get("content", "")
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"delete_chapter_{chapter_id}"):
                            if self.db.delete_chapter(chapter_id):
                                st.success(f"Capítulo {chapter['title']} excluído com sucesso!")
                                if st.session_state.current_chapter == chapter_id:
                                    st.session_state.current_chapter = None
                                    st.session_state.chapter_title = ""
                                    st.session_state.chapter_content = ""
                                st.rerun()
                            else:
                                st.error(f"Erro ao excluir capítulo {chapter['title']}")
            
            st.divider()
            st.subheader("Eventos da Linha do Tempo")
            
            # Botão para criar novo evento
            if st.button("Novo Evento"):
                st.session_state.event_title = ""
                st.session_state.event_description = ""
                st.session_state.event_date = ""
                st.session_state.current_event = None
                st.rerun()
            
            # Lista de eventos
            events = self.db.get_story_timeline_events(story_id)
            if events:
                for event_id, event in events.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"📅 {event['title']}", key=f"event_{event_id}"):
                            st.session_state.current_event = event_id
                            st.session_state.event_title = event.get("title", "")
                            st.session_state.event_description = event.get("description", "")
                            st.session_state.event_date = event.get("date", "")
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"delete_event_{event_id}"):
                            if self.db.delete_timeline_event(event_id):
                                st.success(f"Evento {event['title']} excluído com sucesso!")
                                if st.session_state.current_event == event_id:
                                    st.session_state.current_event = None
                                    st.session_state.event_title = ""
                                    st.session_state.event_description = ""
                                    st.session_state.event_date = ""
                                st.rerun()
                            else:
                                st.error(f"Erro ao excluir evento {event['title']}")
        
        # Área principal
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_chapter_form(story_id)
        
        with col2:
            self._render_timeline_form(story_id)
    
    def _render_story_form(self):
        """Renderiza o formulário de edição da história."""
        with st.form("story_form", clear_on_submit=False):
            st.subheader("Detalhes da História")
            
            # Campos do formulário
            title = st.text_input("Título do Livro", value=st.session_state.story.get("title", ""))
            volume = st.number_input("Número do Volume", min_value=1, value=1)
            genre = st.text_input("Gênero", value=st.session_state.story.get("genre", ""))
            synopsis = st.text_area("Sinopse", value=st.session_state.story.get("synopsis", ""))
            target_audience = st.text_input("Público-Alvo", value=st.session_state.story.get("target_audience", ""))
            main_theme = st.text_input("Tema Principal", value=st.session_state.story.get("main_theme", ""))
            narrative_style = st.text_input("Estilo Narrativo", value=st.session_state.story.get("narrative_style", ""))
            setting = st.text_area("Ambientação", value=st.session_state.story.get("setting", ""))
            
            suggestions = st.text_area(
                "Sugestões para a História (opcional)",
                value=st.session_state.story_suggestions,
                help="Digite sugestões ou ideias para a história. Deixe em branco para geração automática."
            )
            
            # Botões de ação
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Salvar História"):
                    if not title:
                        st.warning("O título do livro é obrigatório.")
                        return
                    
                    self._save_story_info({
                        "title": f"{title} - Volume {volume}",
                        "genre": genre,
                        "synopsis": synopsis,
                        "target_audience": target_audience,
                        "main_theme": main_theme,
                        "narrative_style": narrative_style,
                        "setting": setting,
                        "suggestions": suggestions
                    })
            
            with col2:
                if st.form_submit_button("Gerar Sinopse com IA"):
                    asyncio.run(self._generate_synopsis(title, genre, suggestions))
    
    def _render_chapter_form(self, story_id: str):
        """Renderiza o formulário de edição do capítulo."""
        with st.form("chapter_form", clear_on_submit=False):
            st.subheader("Detalhes do Capítulo")
            
            title = st.text_input("Título", value=st.session_state.chapter_title, key="chapter_title")
            content = st.text_area("Conteúdo", value=st.session_state.chapter_content, key="chapter_content", height=300)
            
            if st.form_submit_button("Salvar Capítulo"):
                if not title:
                    st.warning("O título do capítulo é obrigatório.")
                    return
                
                chapter_data = {
                    "title": title,
                    "content": content,
                    "story_id": story_id
                }
                
                if st.session_state.current_chapter:
                    chapter_data["id"] = st.session_state.current_chapter
                    if self.db.update_chapter(chapter_data):
                        st.success(f"Capítulo {title} atualizado com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar capítulo {title}")
                else:
                    chapter_id = self.db.save_chapter(chapter_data)
                    if chapter_id:
                        st.success(f"Capítulo {title} salvo com sucesso!")
                        st.session_state.current_chapter = chapter_id
                    else:
                        st.error(f"Erro ao salvar capítulo {title}")
                st.rerun()
    
    def _render_timeline_form(self, story_id: str):
        """Renderiza o formulário de edição do evento da linha do tempo."""
        with st.form("timeline_event_form", clear_on_submit=False):
            st.subheader("Evento da Linha do Tempo")
            
            title = st.text_input("Título", value=st.session_state.event_title, key="event_title")
            description = st.text_area("Descrição", value=st.session_state.event_description, key="event_description", height=200)
            date = st.text_input("Data", value=st.session_state.event_date, key="event_date")
            
            if st.form_submit_button("Salvar Evento"):
                if not title:
                    st.warning("O título do evento é obrigatório.")
                    return
                
                event_data = {
                    "title": title,
                    "description": description,
                    "date": date,
                    "story_id": story_id
                }
                
                if st.session_state.current_event:
                    event_data["id"] = st.session_state.current_event
                    if self.db.update_timeline_event(event_data):
                        st.success(f"Evento {title} atualizado com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar evento {title}")
                else:
                    event_id = self.db.save_timeline_event(event_data)
                    if event_id:
                        st.success(f"Evento {title} salvo com sucesso!")
                        st.session_state.current_event = event_id
                    else:
                        st.error(f"Erro ao salvar evento {title}")
                st.rerun()
    
    async def _generate_synopsis(self, title: str, genre: str, suggestions: str = ""):
        """Gera uma sinopse usando IA."""
        if not title or not genre:
            st.warning("Por favor, insira o título e o gênero da história.")
            return
        
        prompt = f"""
        Crie uma sinopse envolvente e profissional para um livro com as seguintes informações:
        Título: {title}
        Gênero: {genre}
        """
        
        if suggestions:
            prompt += f"""
            Sugestões e ideias para a história:
            {suggestions}
            """
        
        prompt += """
        A sinopse deve ser concisa, envolvente e dar uma visão geral da história sem revelar spoilers importantes.
        Mantenha um tom profissional e adequado ao gênero.
        """
        
        try:
            response = await self.llm.generate_response(prompt)
            st.session_state.story["synopsis"] = response
            st.success("Sinopse gerada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao gerar sinopse: {str(e)}")
    
    async def _generate_chapter_content(self, title: str, suggestions: str = ""):
        """Gera o conteúdo do capítulo usando IA."""
        if not title:
            st.warning("Por favor, insira o título do capítulo.")
            return
        
        story = st.session_state.story
        prompt = f"""
        Crie o conteúdo para um capítulo de livro com as seguintes informações:
        
        História: {story.get('title', '')}
        Gênero: {story.get('genre', '')}
        Título do Capítulo: {title}
        """
        
        if suggestions:
            prompt += f"""
            Sugestões e ideias para o capítulo:
            {suggestions}
            """
        
        prompt += """
        O conteúdo deve ser envolvente, manter a consistência com o gênero e estilo da história,
        e avançar a narrativa de forma significativa.
        """
        
        try:
            response = await self.llm.generate_response(prompt)
            st.session_state.chapter_content = response
            st.success("Conteúdo do capítulo gerado com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao gerar conteúdo do capítulo: {str(e)}")
    
    def _save_story_info(self, info: Dict):
        """Salva as informações da história no banco de dados."""
        try:
            story_data = {
                "title": info["title"],
                "description": info["synopsis"],
                "genre": info["genre"],
                "target_audience": info["target_audience"],
                "main_theme": info["main_theme"],
                "narrative_style": info["narrative_style"],
                "setting": info["setting"]
            }
            
            story_id = self.db.save_story(story_data)
            if story_id:
                st.session_state.current_book_id = story_id
                st.success("História salva com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao salvar história.")
        except Exception as e:
            st.error(f"Erro ao salvar história: {e}")
    
    def _save_chapter(self, chapter_data: Dict):
        """Salva os dados do capítulo."""
        if not chapter_data.get("title"):
            st.warning("O título do capítulo é obrigatório.")
            return
        
        chapters = st.session_state.story.get("chapters", [])
        if st.session_state.current_chapter is not None:
            # Atualiza capítulo existente
            chapters[st.session_state.current_chapter] = chapter_data
        else:
            # Adiciona novo capítulo
            chapters.append(chapter_data)
        
        st.session_state.story["chapters"] = chapters
        
        # Salva no banco de dados
        self.db.save_chapter(chapter_data)
        
        st.success("Capítulo salvo com sucesso!")
        st.rerun()
    
    def _save_timeline_event(self, event_data: Dict):
        """Salva os dados do evento da timeline."""
        if not event_data.get("title"):
            st.warning("O título do evento é obrigatório.")
            return
        
        timeline = st.session_state.story.get("timeline", [])
        timeline.append(event_data)
        st.session_state.story["timeline"] = timeline
        
        # Salva no banco de dados
        self.db.save_timeline_event(event_data)
        
        st.success("Evento salvo com sucesso!")
        st.rerun() 