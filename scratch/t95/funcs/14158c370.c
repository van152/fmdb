__int64 __fastcall sub_14158C370(_WORD *a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rsi
  __int64 v12; // rsi
  __int64 v13; // rsi
  __int64 v15; // r12
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
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
  __int64 v35; // rsi
  __int64 v36; // rsi
  __int64 v37; // rsi
  __int16 v38; // ax
  _DWORD v39[18]; // [rsp+40h] [rbp-48h] BYREF

  sub_140814B10(*a2, v39, a1 + 12);
  if ( v39[0] == 0 )
  {
    v11 = *a2;
    (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 64, 1);
    if ( *(_DWORD *)(v11 + 16) == 0 )
    {
      v12 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 129, 1);
      if ( *(_DWORD *)(v12 + 16) == 0 )
      {
        v13 = *a2;
        (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 65, 1);
        if ( *(_DWORD *)(v13 + 16) == 0 )
        {
          v15 = 0;
          while ( 1 )
          {
            v16 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 16], 2);
            if ( *(_DWORD *)(v16 + 16) != 0 )
              break;
            v17 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 17], 1);
            if ( *(_DWORD *)(v17 + 16) != 0 )
              break;
            v18 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 17] + 1,
              1);
            if ( *(_DWORD *)(v18 + 16) != 0 )
              break;
            v19 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 18], 1);
            if ( *(_DWORD *)(v19 + 16) != 0 )
              break;
            v20 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 18] + 1,
              1);
            if ( *(_DWORD *)(v20 + 16) != 0 )
              break;
            v21 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 19], 1);
            if ( *(_DWORD *)(v21 + 16) != 0 )
              break;
            v22 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 19] + 1,
              1);
            if ( *(_DWORD *)(v22 + 16) != 0 )
              break;
            v23 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 20], 1);
            if ( *(_DWORD *)(v23 + 16) != 0 )
              break;
            v24 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 20] + 1,
              1);
            if ( *(_DWORD *)(v24 + 16) != 0 )
              break;
            v25 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 21], 1);
            if ( *(_DWORD *)(v25 + 16) != 0 )
              break;
            v26 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 21] + 1,
              1);
            if ( *(_DWORD *)(v26 + 16) != 0 )
              break;
            v27 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 22], 1);
            if ( *(_DWORD *)(v27 + 16) != 0 )
              break;
            v28 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 22] + 1,
              1);
            if ( *(_DWORD *)(v28 + 16) != 0 )
              break;
            v29 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 23], 1);
            if ( *(_DWORD *)(v29 + 16) != 0 )
              break;
            v30 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 23] + 1,
              1);
            if ( *(_DWORD *)(v30 + 16) != 0 )
              break;
            v31 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 24], 1);
            if ( *(_DWORD *)(v31 + 16) != 0 )
              break;
            v32 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 24] + 1,
              1);
            if ( *(_DWORD *)(v32 + 16) != 0 )
              break;
            v33 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 25], 1);
            if ( *(_DWORD *)(v33 + 16) != 0 )
              break;
            v34 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 25] + 1,
              1);
            if ( *(_DWORD *)(v34 + 16) != 0 )
              break;
            v35 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 26], 1);
            if ( *(_DWORD *)(v35 + 16) != 0 )
              break;
            v36 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              *a2,
              (__int64)&a1[v15 + 26] + 1,
              1);
            if ( *(_DWORD *)(v36 + 16) != 0 )
              break;
            v37 = *a2;
            (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &a1[v15 + 27], 1);
            if ( *(_DWORD *)(v37 + 16) != 0 )
              break;
            sub_14158C770(&a1[v15 + 16]);
            v15 += 12;
            if ( v15 == 48 )
            {
              v38 = a1[16];
              if ( v38 == a1[28] && v38 == a1[40] && v38 == a1[52] )
              {
                a1[16] = 55;
                a1[28] = 145;
                a1[40] = 230;
                a1[52] = 300;
              }
              return sub_140FAED40((_DWORD)a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
            }
          }
        }
      }
    }
  }
  return 0;
}
