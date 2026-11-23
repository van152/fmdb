bool __fastcall sub_1444A5480(_BYTE *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  _DWORD *v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  _BYTE v18[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v18, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v6 = (_DWORD *)*a2;
  if ( v18[0] > 1u )
  {
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)v6 + 40LL))(a1: *a2, a2: a1, a3: 1);
    if ( v6[4] == 0 )
    {
      v7 = *a2;
      (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 1, a3: 1);
      if ( *(_DWORD *)(v7 + 16) == 0 )
      {
        v8 = *a2;
        (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 2, a3: 1);
        if ( *(_DWORD *)(v8 + 16) == 0 )
        {
          v9 = *a2;
          (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 3, a3: 1);
          if ( *(_DWORD *)(v9 + 16) == 0 )
          {
            v10 = *a2;
            (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 4, a3: 1);
            if ( *(_DWORD *)(v10 + 16) == 0 )
            {
              v11 = *a2;
              (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 5, a3: 1);
              if ( *(_DWORD *)(v11 + 16) == 0 )
              {
                v12 = *a2;
                (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 6, a3: 1);
                if ( *(_DWORD *)(v12 + 16) == 0 )
                  return *(_DWORD *)(*a2 + 16LL) == 0;
              }
            }
          }
        }
      }
    }
    return false;
  }
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)v6 + 40LL))(a1: *a2, a2: a1 + 1, a3: 1);
  if ( v6[4] != 0 )
    return false;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 2, a3: 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return false;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 3, a3: 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return false;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 4, a3: 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return false;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 5, a3: 1);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return false;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 6, a3: 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return false;
  *a1 = a1[1];
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
