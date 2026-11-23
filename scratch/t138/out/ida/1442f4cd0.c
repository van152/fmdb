bool __fastcall sub_1442F4CD0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  _DWORD *v11; // rdi
  __int64 v12; // rbx
  __int64 v13; // rbx
  _BYTE v14[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v14, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  if ( v14[0] > 3u || HIWORD(qword_141B6034C) == 0 )
  {
    if ( (unsigned __int8)sub_140F92E30(
                            a1: (unsigned int)&qword_141B5FDA8,
                            a2: a1,
                            a3: (_DWORD)a2,
                            a4: qword_141B5FDD0,
                            a5: 1) != 0
      && (unsigned __int8)sub_140F83A50(a1: a1 + 8, a2) != 0
      && (unsigned __int8)sub_140F926F0(
                            a1: (unsigned int)&qword_141B5FDA8,
                            a2: (int)a1 + 16,
                            a3: (_DWORD)a2,
                            a4: qword_141B5FDB8,
                            a5: 1) != 0 )
    {
      v12 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 36, a3: 1);
      if ( *(_DWORD *)(v12 + 16) == 0
        && (unsigned __int8)sub_140DB8980(a1: a1 + 32, a2) != 0
        && (unsigned __int8)sub_140F83A50(a1: a1 + 24, a2) != 0 )
      {
        v13 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 37, a3: 1);
        if ( *(_DWORD *)(v13 + 16) == 0 )
        {
          v11 = (_DWORD *)*a2;
          return v11[4] == 0;
        }
      }
    }
    return false;
  }
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 24, a3: 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 32, a2) == 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 36, a3: 1);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return false;
  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(a1: v11, a2: a1 + 37, a3: 1);
  return v11[4] == 0;
}
