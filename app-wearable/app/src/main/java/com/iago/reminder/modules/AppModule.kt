package com.iago.reminder.modules

import com.iago.reminder.BuildConfig
import com.iago.reminder.api.ReminderApi
import com.iago.reminder.repository.ReminderRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@InstallIn(SingletonComponent::class)
@Module
object AppModule {

    @Singleton
    @Provides
    fun provideRepository(api: ReminderApi) = ReminderRepository(api)

    @Singleton
    @Provides
    fun provideApi(): ReminderApi = Retrofit.Builder()
        .addConverterFactory((GsonConverterFactory.create()))
        .baseUrl(BuildConfig.API_BASE_URL)
        .build()
        .create(ReminderApi::class.java)


}