__int64 __fastcall sub_141053680(__int64 a1, _QWORD *a2, unsigned int a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v12; // rsi
  int v13; // edi
  __int64 v14; // rsi
  int v15; // edi
  __int64 v16; // rsi
  int v17; // edi
  __int64 v18; // rsi
  __int64 v19; // rsi
  int v20; // edi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // rsi
  __int64 v28; // rsi
  __int64 v29; // rsi
  __int64 v30; // rsi
  __int64 v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rsi
  __int64 v34; // rsi
  char v35; // si
  char v37; // [rsp+47h] [rbp-51h] BYREF
  __int64 v38; // [rsp+48h] [rbp-50h] BYREF
  char v39; // [rsp+50h] [rbp-48h]

  if ( a7 != 0 )
  {
    v12 = *a2;
    if ( *a2 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v12 + 8));
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v12 + 40LL))(v12, a1 + 184, 4);
    }
    v13 = *(_DWORD *)(v12 + 16);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v12 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v12)(v12, 1);
    if ( v13 != 0 )
      return 0;
    v14 = *a2;
    if ( *a2 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v14 + 8));
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v14 + 40LL))(v14, a1 + 188, 4);
    }
    v15 = *(_DWORD *)(v14 + 16);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v14)(v14, 1);
    if ( v15 != 0 )
      return 0;
    v16 = *a2;
    if ( *a2 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v16 + 8));
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v16 + 40LL))(v16, a1 + 220, 4);
    }
    v17 = *(_DWORD *)(v16 + 16);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v16 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v16)(v16, 1);
    if ( v17 != 0 )
      return 0;
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 224, 1);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      return 0;
    v19 = *a2;
    if ( *a2 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v19 + 8));
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v19 + 40LL))(v19, a1 + 192, 4);
    }
    v20 = *(_DWORD *)(v19 + 16);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v19 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v19)(v19, 1);
    if ( v20 != 0 )
      return 0;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 204, 4);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      return 0;
    v22 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 208, 4);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      return 0;
    v23 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 212, 4);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      return 0;
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 216, 4);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      return 0;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 196, 4);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return 0;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 200, 4);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return 0;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 225, 1);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return 0;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 226, 1);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return 0;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 228, 1);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return 0;
    v30 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 229, 1);
    if ( *(_DWORD *)(v30 + 16) != 0 )
      return 0;
    v31 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 230, 1);
    if ( *(_DWORD *)(v31 + 16) != 0 )
      return 0;
    v32 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 231, 1);
    if ( *(_DWORD *)(v32 + 16) != 0 )
      return 0;
    v33 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 227, 1);
    if ( *(_DWORD *)(v33 + 16) != 0 )
      return 0;
    v34 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v37, 1);
    if ( *(_DWORD *)(v34 + 16) != 0 )
      return 0;
    if ( v37 > 0 )
    {
      v35 = 0;
      do
      {
        v38 = -1;
        v39 = 0;
        if ( (unsigned __int8)sub_141053A80(&v38, a2) == 0 )
          return 0;
        sub_1408E73B0(a1 + 232, &v38);
      }
      while ( ++v35 < v37 );
    }
  }
  if ( (_BYTE)a3 == 0
    || (a3 = 0, (unsigned __int8)sub_1411A1280(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8) != 0)
    && (a3 = 0, (unsigned __int8)sub_1411C2780(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8) != 0) )
  {
    LOBYTE(a3) = 1;
  }
  return a3;
}
