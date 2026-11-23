char __fastcall sub_144519690(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  int v8; // ebp
  __int64 v9; // rbx
  int v10; // ebp
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  int *v17; // r14
  __int64 v18; // rbx
  int v19; // eax
  __int64 v20; // rbx
  __int16 v21; // cx
  _DWORD *v22; // rbx
  int *v23; // rdi
  int v24; // ecx
  __int64 v25; // rcx
  _DWORD v27[11]; // [rsp+2Ch] [rbp-2Ch] BYREF

  v4 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(v4, a1 + 24, 4);
  if ( v4[4] != 0 )
    goto LABEL_26;
  if ( (unsigned __int16)qword_141B60330 >= 0xDDDu )
  {
    v5 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 40, 4);
    if ( v5[4] != 0 )
      goto LABEL_26;
  }
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    goto LABEL_26;
  v7 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v7 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v7 + 40LL))(v7, a1 + 48, 4);
  }
  v8 = *(_DWORD *)(v7 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v7 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v7)(v7, 1);
  if ( v8 != 0 )
    goto LABEL_26;
  v9 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v9 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v9 + 40LL))(v9, a1 + 52, 4);
  }
  v10 = *(_DWORD *)(v9 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v9 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v9)(v9, 1);
  if ( v10 != 0 || (unsigned __int8)sub_14156AB70(a1 + 56, a2) == 0 )
    goto LABEL_26;
  if ( (unsigned __int16)qword_141B60330 >= 0xDDDu )
  {
    v11 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 72, 8);
    if ( *(_DWORD *)(v11 + 16) == 0 )
      goto LABEL_21;
LABEL_26:
    LOBYTE(v19) = 0;
    return v19;
  }
  v27[0] = 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v27, 4);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    goto LABEL_26;
  *(_QWORD *)(a1 + 72) = v27[0];
LABEL_21:
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 102, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    goto LABEL_26;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 88, 4);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    goto LABEL_26;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 92, 4);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    goto LABEL_26;
  v16 = *a2;
  v17 = (int *)(a1 + 100);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 100, 2);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    goto LABEL_26;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 84, 4);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    goto LABEL_26;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 103, 1);
  LOWORD(v19) = 0;
  if ( *(_DWORD *)(v20 + 16) == 0 )
  {
    if ( (__int16)*v17 > 0 )
      v19 = *v17;
    v21 = 400;
    if ( (__int16)v19 < 400 )
      v21 = v19;
    *(_WORD *)v17 = v21;
    if ( (unsigned __int16)qword_141B60330 >= 0xDDAu )
    {
      v22 = (_DWORD *)*a2;
      v23 = (int *)(a1 + 96);
      (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v22 + 40LL))(v22, a1 + 96, 4);
      v19 = 0;
      if ( v22[4] != 0 )
        return v19;
      if ( *v23 > 0 )
        v19 = *v23;
      v24 = 400;
      if ( v19 < 400 )
        v24 = v19;
      *v23 = v24;
    }
    v25 = *(_QWORD *)(a1 + 24);
    LOBYTE(v19) = 1;
    if ( (int)v25 >= 0 || *(_DWORD *)(a1 + 80) == -1 )
      *(_DWORD *)(a1 + 80) = v25;
  }
  return v19;
}
