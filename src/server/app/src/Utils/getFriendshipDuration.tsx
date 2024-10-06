// src/utils/getFriendshipDuration.ts
import { User } from '../types/User';

export const getFriendshipDuration = (user: User): string => {
  if (!user.friendshipStartDate) return '';
  const diff = new Date().getTime() - user.friendshipStartDate.getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  return `${days} day(s) of friendship`;
};
