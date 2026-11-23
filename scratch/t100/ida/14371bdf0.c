int *__fastcall sub_14371BDF0(_DWORD *a1, int *a2, __int64 *a3)
{
  __int64 v6; // rax
  int v7; // edx
  int v8; // ecx
  __int64 v9; // rdx
  volatile signed __int32 *v10; // rcx
  volatile signed __int32 *v11; // r12
  __int64 v12; // rax
  int v13; // eax
  __int64 v14; // rdx
  __int64 v15; // rax
  volatile signed __int32 *v16; // rcx
  volatile signed __int32 *v17; // rbx
  volatile signed __int32 *v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // r15
  __int64 v21; // rcx
  volatile signed __int32 *v23; // [rsp+20h] [rbp-20h]
  __int64 v24; // [rsp+28h] [rbp-18h] BYREF
  unsigned int v25; // [rsp+34h] [rbp-Ch] BYREF
  __int64 v26; // [rsp+38h] [rbp-8h]

  v26 = -2;
  v25 = 0;
  (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, &v25, 4);
  if ( qword_141AA7808 > (unsigned __int64)v25 )
  {
    if ( a1[4] != 0 || v25 == 0 )
    {
      if ( a3 != &qword_141B59EE0 )
      {
        v14 = qword_141B59EE0;
        v15 = *a3;
        v16 = (volatile signed __int32 *)(*a3 - 4);
        if ( *a3 == 0 )
          v16 = nullptr;
        v17 = (volatile signed __int32 *)(qword_141B59EE0 - 4);
        if ( qword_141B59EE0 != 0 )
        {
          if ( v15 != 0 && _InterlockedDecrement(v16) == 0 )
            sub_1412EC9A0(v16, v14);
          *a3 = 0;
          _InterlockedIncrement(v17);
          v18 = v17 + 1;
        }
        else
        {
          if ( v15 != 0 && _InterlockedDecrement(v16) == 0 )
            sub_1412EC9A0(v16, 0);
          v18 = nullptr;
        }
        *a3 = (__int64)v18;
      }
      goto LABEL_48;
    }
    v6 = sub_1412EC810(264);
    v7 = v25;
    *(_DWORD *)v6 = 0;
    v8 = 0;
    if ( v7 > 0 )
      v8 = v7;
    *(_DWORD *)(v6 + 4) = v8;
    *(_BYTE *)(v6 + 8) = 0;
    _InterlockedIncrement((volatile signed __int32 *)v6);
    v23 = (volatile signed __int32 *)v6;
    (*(void (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a1 + 40LL))(a1, v6 + 8, v25);
    v11 = v23;
    *((_BYTE *)v23 + v25 + 8) = 0;
    _InterlockedIncrement(v23);
    v12 = *a3;
    if ( (volatile signed __int32 *)*a3 == v23 + 1 )
    {
      if ( _InterlockedDecrement(v23) == 0 )
        sub_1412EC9A0(v23, v9);
    }
    else
    {
      v10 = (volatile signed __int32 *)(v12 - 4);
      if ( v12 != 0 )
      {
        if ( _InterlockedDecrement(v10) == 0 )
          sub_1412EC9A0(v10, v9);
      }
      else
      {
        v10 = nullptr;
      }
      *a3 = (__int64)(v23 + 1);
    }
    v19 = qword_141B59FA0;
    if ( qword_141B59FA0 == 0 || *(_QWORD *)(qword_141B59FA0 + 8) == 0 )
    {
LABEL_46:
      if ( _InterlockedDecrement(v11) == 0 )
        sub_1412EC9A0(v11, v9);
LABEL_48:
      v13 = a1[4];
      goto LABEL_49;
    }
    v20 = *(_QWORD *)(qword_141B59FA0 + 16);
    if ( v20 == (unsigned int)MEMORY[0x141947498](v10) )
    {
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64 *))(**(_QWORD **)(v19 + 8) + 8LL))(
        *(_QWORD *)(v19 + 8),
        &v24,
        a3);
      v21 = v24;
      v11 = v23;
    }
    else
    {
      v24 = 0;
      v21 = *a3;
      if ( &v24 == a3 )
      {
        if ( v21 == 0 )
          goto LABEL_46;
LABEL_43:
        if ( _InterlockedDecrement((volatile signed __int32 *)(v21 - 4)) == 0 )
          sub_1412EC9A0(v21 - 4, v9);
LABEL_45:
        *a3 = v24;
        goto LABEL_46;
      }
      if ( v21 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v21 - 4));
      v24 = v21;
    }
    if ( *a3 == v21 )
    {
      if ( v21 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 - 4)) == 0 )
        sub_1412EC9A0(v21 - 4, v9);
      goto LABEL_46;
    }
    v21 = *a3;
    if ( *a3 == 0 )
      goto LABEL_45;
    goto LABEL_43;
  }
  a1[4] = 1;
  v13 = 1;
LABEL_49:
  *a2 = v13;
  return a2;
}
