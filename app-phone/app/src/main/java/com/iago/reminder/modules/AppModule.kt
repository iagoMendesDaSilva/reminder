package com.iago.reminder.modules

import android.content.Context
import androidx.room.Room
import com.iago.reminder.BuildConfig
import com.iago.reminder.api.ReminderApi
import com.iago.reminder.database.ReminderDao
import com.iago.reminder.database.ReminderDatabase
import com.iago.reminder.repository.UserRepository
import com.iago.reminder.repository.WordRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@InstallIn(SingletonComponent::class)
@Module
object AppModule {

    @Singleton
    @Provides
    fun provideAppDatabase(@ApplicationContext context: Context): ReminderDatabase =
        Room.databaseBuilder(
            context,
            ReminderDatabase::class.java,
            "reminder_db"
        )
            .fallbackToDestructiveMigration()
            .build()

    @Singleton
    @Provides
    fun provideReminderDao(reminderDatabase: ReminderDatabase): ReminderDao =
        reminderDatabase.getDao()

    @Singleton
    @Provides
    fun provideUserRepository(api: ReminderApi) = UserRepository(api)

    @Singleton
    @Provides
    fun provideWordRepository(api: ReminderApi) = WordRepository(api)

    @Singleton
    @Provides
    fun provideApi(): ReminderApi = Retrofit.Builder()
        .addConverterFactory((GsonConverterFactory.create()))
        .baseUrl(BuildConfig.API_BASE_URL)
        .build()
        .create(ReminderApi::class.java)


}