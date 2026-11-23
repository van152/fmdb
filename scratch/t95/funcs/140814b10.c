// THUNK ALIAS -> sub_14371BDF0 (jmp:0x140814b10->0x14371bdf0)
int *__fastcall sub_14371BDF0(_DWORD *a1, int *a2, __int64 *a3)
{
  __int64 v6; // rax
  int v7; // edx
  int v8; // ecx
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v10; // r12
  __int64 v11; // rax
  int v12; // eax
  __int64 v13; // rax
  volatile signed __int32 *v14; // rcx
  volatile signed __int32 *v15; // rbx
  volatile signed __int32 *v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // r15
  __int64 v19; // rcx
  volatile signed __int32 *v21; // [rsp+20h] [rbp-20h]
  __int64 v22; // [rsp+28h] [rbp-18h] BYREF
  unsigned int v23; // [rsp+34h] [rbp-Ch] BYREF
  __int64 v24; // [rsp+38h] [rbp-8h]

  v24 = -2;
  v23 = 0;
  (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, &v23, 4);
  if ( qword_141AA7808 > (unsigned __int64)v23 )
  {
    if ( a1[4] != 0 || v23 == 0 )
    {
      if ( a3 != &qword_141B59EE0 )
      {
        v13 = *a3;
        v14 = (volatile signed __int32 *)(*a3 - 4);
        if ( *a3 == 0 )
          v14 = nullptr;
        v15 = (volatile signed __int32 *)(qword_141B59EE0 - 4);
        if ( qword_141B59EE0 != 0 )
        {
          if ( v13 != 0 && _InterlockedDecrement(v14) == 0 )
            sub_1412EC9A0((__int64)v14);
          *a3 = 0;
          _InterlockedIncrement(v15);
          v16 = v15 + 1;
        }
        else
        {
          if ( v13 != 0 && _InterlockedDecrement(v14) == 0 )
            sub_1412EC9A0((__int64)v14);
          v16 = nullptr;
        }
        *a3 = (__int64)v16;
      }
      goto LABEL_48;
    }
    v6 = sub_1412EC810(264, v23);
    v7 = v23;
    *(_DWORD *)v6 = 0;
    v8 = 0;
    if ( v7 > 0 )
      v8 = v7;
    *(_DWORD *)(v6 + 4) = v8;
    *(_BYTE *)(v6 + 8) = 0;
    _InterlockedIncrement((volatile signed __int32 *)v6);
    v21 = (volatile signed __int32 *)v6;
    (*(void (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a1 + 40LL))(a1, v6 + 8, v23);
    v10 = v21;
    *((_BYTE *)v21 + v23 + 8) = 0;
    _InterlockedIncrement(v21);
    v11 = *a3;
    if ( (volatile signed __int32 *)*a3 == v21 + 1 )
    {
      if ( _InterlockedDecrement(v21) == 0 )
        sub_1412EC9A0((__int64)v21);
    }
    else
    {
      v9 = (volatile signed __int32 *)(v11 - 4);
      if ( v11 != 0 )
      {
        if ( _InterlockedDecrement(v9) == 0 )
          sub_1412EC9A0((__int64)v9);
      }
      else
      {
        v9 = nullptr;
      }
      *a3 = (__int64)(v21 + 1);
    }
    v17 = qword_141B59FA0;
    if ( qword_141B59FA0 == 0 || *(_QWORD *)(qword_141B59FA0 + 8) == 0 )
    {
LABEL_46:
      if ( _InterlockedDecrement(v10) == 0 )
        sub_1412EC9A0((__int64)v10);
LABEL_48:
      v12 = a1[4];
      goto LABEL_49;
    }
    v18 = *(_QWORD *)(qword_141B59FA0 + 16);
    if ( v18 == (unsigned int)MEMORY[0x141947498](v9) )
    {
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64 *))(**(_QWORD **)(v17 + 8) + 8LL))(
        *(_QWORD *)(v17 + 8),
        &v22,
        a3);
      v19 = v22;
      v10 = v21;
    }
    else
    {
      v22 = 0;
      v19 = *a3;
      if ( &v22 == a3 )
      {
        if ( v19 == 0 )
          goto LABEL_46;
LABEL_43:
        if ( _InterlockedDecrement((volatile signed __int32 *)(v19 - 4)) == 0 )
          sub_1412EC9A0(v19 - 4);
LABEL_45:
        *a3 = v22;
        goto LABEL_46;
      }
      if ( v19 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v19 - 4));
      v22 = v19;
    }
    if ( *a3 == v19 )
    {
      if ( v19 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 - 4)) == 0 )
        sub_1412EC9A0(v19 - 4);
      goto LABEL_46;
    }
    v19 = *a3;
    if ( *a3 == 0 )
      goto LABEL_45;
    goto LABEL_43;
  }
  a1[4] = 1;
  v12 = 1;
LABEL_49:
  *a2 = v12;
  return a2;
}
