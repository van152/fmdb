bool __fastcall sub_144749220(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v8; // rbx
  unsigned __int8 v9; // al
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  unsigned int v14; // ebx
  __int64 v15; // rbx
  unsigned __int8 v16; // [rsp+2Eh] [rbp-1Ah] BYREF
  _BYTE v17[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v16, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 12, a3: 2);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  if ( v16 >= 2u )
  {
    v8 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 4, a3: 4);
    if ( *(_DWORD *)(v8 + 16) == 0 )
    {
      v9 = v16;
      if ( v16 >= 5u )
      {
        v10 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
        if ( *(_DWORD *)(v10 + 16) != 0 )
          return false;
        v9 = v16;
      }
      if ( v9 < 3u )
      {
        v17[0] = 0;
        v13 = *a2;
        (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v17, a3: 1);
        if ( *(_DWORD *)(v13 + 16) != 0 )
          return false;
        v14 = v17[0];
        *(_BYTE *)(a1 + 14) = sub_141454210(a1: v17[0]);
        *(_BYTE *)(a1 + 15) = sub_141454230(a1: *(unsigned __int16 *)(a1 + 12), a2: v14);
      }
      else
      {
        v11 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 14, a3: 1);
        if ( *(_DWORD *)(v11 + 16) != 0 )
          return false;
        v12 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 15, a3: 1);
        if ( *(_DWORD *)(v12 + 16) != 0 )
          return false;
      }
      if ( v16 < 4u )
        return *(_DWORD *)(*a2 + 16LL) == 0;
      v15 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 1);
      if ( *(_DWORD *)(v15 + 16) == 0 )
        return *(_DWORD *)(*a2 + 16LL) == 0;
    }
    return false;
  }
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
