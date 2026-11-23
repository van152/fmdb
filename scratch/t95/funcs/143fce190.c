__int64 __fastcall sub_143FCE190(
        _QWORD *a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        char a7,
        __int64 a8)
{
  _QWORD *v9; // rsi
  volatile signed __int32 *v10; // rbx
  volatile signed __int32 *v11; // rbx
  volatile signed __int32 *v12; // rbx
  volatile signed __int32 *v13; // rbx
  volatile signed __int32 *v14; // rbx
  volatile signed __int32 *v15; // rbx
  volatile signed __int32 *v16; // rbx
  volatile signed __int32 *v17; // rbx
  volatile signed __int32 *v18; // rbx
  volatile signed __int32 *v19; // rbx
  volatile signed __int32 *v20; // rbx
  volatile signed __int32 *v21; // rbx
  volatile signed __int32 *v22; // rbx
  volatile signed __int32 *v23; // rbx
  volatile signed __int32 *v24; // rdi
  unsigned int *v25; // rbx
  __int64 v26; // r8

  v9 = a1;
  if ( a7 == 0 )
    goto LABEL_17;
  a1[5] = 0;
  a1[4] = 0;
  a1[3] = 0;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 3, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_16;
  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 4, 4);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_16;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 5, 4);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_16;
  v13 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
    *a2,
    (__int64)v9 + 54,
    2);
  if ( *((_DWORD *)v13 + 4) != 0 )
    goto LABEL_16;
  v14 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
    *a2,
    (__int64)v9 + 57,
    1);
  if ( *((_DWORD *)v14 + 4) != 0 )
    goto LABEL_16;
  v15 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
    *a2,
    (__int64)v9 + 58,
    1);
  if ( *((_DWORD *)v15 + 4) != 0 )
    goto LABEL_16;
  v16 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
    *a2,
    (__int64)v9 + 59,
    1);
  if ( *((_DWORD *)v16 + 4) != 0 )
    goto LABEL_16;
  v17 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
    *a2,
    (__int64)v9 + 60,
    1);
  if ( *((_DWORD *)v17 + 4) != 0 )
    goto LABEL_16;
  v18 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
    *a2,
    (__int64)v9 + 61,
    1);
  if ( *((_DWORD *)v18 + 4) != 0 )
    goto LABEL_16;
  v19 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 6, 2);
  if ( *((_DWORD *)v19 + 4) != 0 )
    goto LABEL_16;
  v20 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
    *a2,
    (__int64)v9 + 50,
    2);
  if ( *((_DWORD *)v20 + 4) != 0
    || (v21 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
          *a2,
          (__int64)v9 + 52,
          2),
        *((_DWORD *)v21 + 4) != 0)
    || (v22 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 7, 1),
        *((_DWORD *)v22 + 4) != 0)
    || (v23 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
          *a2,
          (__int64)v9 + 62,
          1),
        *((_DWORD *)v23 + 4) != 0) )
  {
LABEL_16:
    LODWORD(v9) = 0;
  }
  else
  {
LABEL_17:
    v24 = *a2;
    if ( v24 != nullptr )
    {
      _InterlockedIncrement(v24 + 2);
      v25 = (unsigned int *)(v9 + 1);
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v24 + 40LL))(v24, v9 + 1, 12);
    }
    else
    {
      v25 = (unsigned int *)(v9 + 1);
    }
    v26 = *v25;
    if ( (unsigned int)v26 >= 0x989681 )
    {
      v26 = a6;
      *v25 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, _QWORD *, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v26, a4);
    }
    LOBYTE(v9) = 1;
    if ( v24 != nullptr && _InterlockedDecrement(v24 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v24)(v24, 1);
  }
  return (unsigned int)v9;
}
