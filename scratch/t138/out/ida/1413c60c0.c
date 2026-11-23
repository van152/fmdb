char __fastcall sub_1413C60C0(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v13; // rax
  _BYTE v14[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: a1 + 20, a3: 2);
  if ( v4[4] != 0 )
    return 0;
  v5 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 28, a3: 1);
  if ( v5[4] != 0 )
    return 0;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 29, a3: 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return 0;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 22, a3: 2);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return 0;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 26, a3: 1);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return 0;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 24, a3: 2);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 16, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_1413C6240(a1, a2) == 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 27, a3: 1);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v14, a3: 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  if ( v14[0] != 0
    && (v13 = sub_140B526C0(a1: 40),
        *(_QWORD *)v13 = 0,
        *(_QWORD *)(v13 + 8) = 0,
        *(_QWORD *)(v13 + 16) = 0,
        *(_DWORD *)(v13 + 24) = 124518401,
        *(_QWORD *)(v13 + 28) = 0x4FFFFFFFFFFFFLL,
        *(_QWORD *)(a1 + 8) = v13,
        (unsigned __int8)sub_141353D50(a1: v13, a2) == 0) )
  {
    return 0;
  }
  else
  {
    return 1;
  }
}
