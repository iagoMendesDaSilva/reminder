package com.iago.reminder.screens.splash

import android.content.Context
import android.view.animation.OvershootInterpolator
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.AnimationVector1D
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.platform.LocalContext
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavHostController
import com.iago.reminder.BuildConfig
import com.iago.reminder.helpers.Logo
import com.onesignal.OneSignal
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

@Composable
fun SplashScreen(navController: NavHostController) {

    val context=LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    var scale = remember { Animatable(0f) }
    val splashViewModel = hiltViewModel<SplashViewModel>()

    LaunchedEffect(key1 = true, block = {
        configOnesignal(context)
        verifyLogin(scale, navController, splashViewModel, coroutineScope)
    })

    Surface(
        modifier = Modifier
            .fillMaxSize()
            .scale(scale.value),
        color = MaterialTheme.colors.background,
    ) {
        Logo()
    }
}

fun configOnesignal(context: Context) {
    OneSignal.initWithContext(context)
    OneSignal.setAppId(BuildConfig.ONESIGNAL_APP_ID)
    OneSignal.setLogLevel(OneSignal.LOG_LEVEL.VERBOSE, OneSignal.LOG_LEVEL.NONE)
}

suspend fun verifyLogin(
    scale: Animatable<Float, AnimationVector1D>,
    navController: NavHostController,
    splashViewModel: SplashViewModel,
    coroutineScope: CoroutineScope
) {
    animateSplah(scale, .8f, 3f, 1600)
    splashViewModel.verifyUser(navController){
        coroutineScope.launch {
            animateSplah(scale, 0f, 0f, 600)
        }
    }
}

suspend fun animateSplah(
    scale: Animatable<Float, AnimationVector1D>,
    toValue: Float,
    tension: Float,
    duration: Int
) {
    scale.animateTo(
        toValue,
        animationSpec = tween(durationMillis = duration, easing = {
            OvershootInterpolator(tension)
                .getInterpolation(it)
        })
    )
}