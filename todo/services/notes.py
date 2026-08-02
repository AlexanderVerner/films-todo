import logging
from typing import Protocol

from django.contrib.auth.models import User
from django.http import Http404

from todo.models import Note, Movie

logger = logging.getLogger(__name__)


class NoteService:
    """Service for managing notes (user's movie watchlist)."""

    @staticmethod
    def get_note_list(user: User) -> list[Note]:
        """Fetch all notes for a user with related movies to avoid N+1 queries.
        
        Args:
            user: User object to fetch notes for
            
        Returns:
            List of Note objects with related Movie data preloaded
        """
        return Note.objects.filter(user=user).select_related('movie').all()

    @staticmethod
    def get_note(note_id: int, user: User) -> Note:
        """Fetch a specific note by id, ensuring it belongs to the user.
        
        Args:
            note_id: ID of the note to fetch
            user: User object to verify ownership
            
        Returns:
            Note object with related Movie data preloaded
            
        Raises:
            Http404: If note doesn't exist or doesn't belong to the user
        """
        try:
            return Note.objects.select_related('movie').get(id=note_id, user=user)
        except Note.DoesNotExist:
            logger.warning('note_not_found', extra={'note_id': note_id, 'user_id': user.id})
            raise Http404(f"Note with id {note_id} not found")

    @staticmethod
    def create_note(user: User, movie: Movie) -> Note:
        """Create or get a note for a user and movie.
        
        Args:
            user: User who owns the note
            movie: Movie to associate with the note
            
        Returns:
            Note object (created or existing)
        """
        note, created = Note.objects.get_or_create(user=user, movie=movie)
        action = 'created' if created else 'updated'
        logger.info(
            f'note_{action}',
            extra={
                'note_id': note.id,
                'user_id': user.id,
                'movie_id': movie.id,
            }
        )
        return note

    @staticmethod
    def delete_note(note_id: int, user: User) -> None:
        """Delete a note by id, ensuring it belongs to the user.
        
        Args:
            note_id: ID of the note to delete
            user: User object to verify ownership
            
        Raises:
            Http404: If note doesn't exist or doesn't belong to the user
        """
        try:
            note = Note.objects.get(id=note_id, user=user)
            note.delete()
            logger.info('note_deleted', extra={'note_id': note_id, 'user_id': user.id})
        except Note.DoesNotExist:
            logger.warning('note_not_found_on_delete', extra={'note_id': note_id, 'user_id': user.id})
            raise Http404(f"Note with id {note_id} not found")
