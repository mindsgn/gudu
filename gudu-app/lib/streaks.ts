type StreakProfile = {
  currentStreak: number;
  longestStreak: number;
  lastActiveOn: string | null;
};

type StreakUpdate = {
  currentStreak: number;
  longestStreak: number;
  lastActiveOn: string;
};

const toDateKey = (date: Date): string => {
  const year = date.getFullYear();
  const month = `${date.getMonth() + 1}`.padStart(2, "0");
  const day = `${date.getDate()}`.padStart(2, "0");

  return `${year}-${month}-${day}`;
};

const shiftDateKey = (dateKey: string, days: number): string => {
  const [year, month, day] = dateKey.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  date.setDate(date.getDate() + days);
  return toDateKey(date);
};

export const getLocalDateKey = (date: Date): string => {
  return toDateKey(date);
};

export const getUpdatedStreak = (
  profile: StreakProfile,
  activityDate: string,
  alreadyHadActivityToday: boolean,
): StreakUpdate => {
  if (alreadyHadActivityToday) {
    return {
      currentStreak: profile.currentStreak,
      longestStreak: profile.longestStreak,
      lastActiveOn: activityDate,
    };
  }

  const previousDate = profile.lastActiveOn;
  const expectedPreviousDate = shiftDateKey(activityDate, -1);
  const currentStreak =
    previousDate === expectedPreviousDate ? profile.currentStreak + 1 : 1;
  const longestStreak = Math.max(profile.longestStreak, currentStreak);

  return {
    currentStreak,
    longestStreak,
    lastActiveOn: activityDate,
  };
};
