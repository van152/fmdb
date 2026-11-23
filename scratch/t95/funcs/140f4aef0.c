__int64 __fastcall sub_140F4AEF0(__int64 a1, int a2, _QWORD *a3)
{
  __int64 v6; // rax
  __int64 *v7; // rbx
  __int64 *v8; // rdi
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 *v11; // rbx
  __int64 *v12; // rsi
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rax
  __int64 v16; // rax
  __int64 v17; // rcx
  int v18; // ebx
  __int64 *v19; // rax
  __int64 *v20; // rsi
  _QWORD *v21; // rsi
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v25; // [rsp+20h] [rbp-30h] BYREF
  __int64 v26; // [rsp+28h] [rbp-28h]
  __int64 v27; // [rsp+38h] [rbp-18h] BYREF
  int v28; // [rsp+40h] [rbp-10h]
  __int64 v29; // [rsp+48h] [rbp-8h]

  v29 = -2;
  sub_1407C9510(&v25);
  v6 = qword_141B60C30;
  v7 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v6 != 1685353593 )
    {
      v6 += 16;
      if ( v6 == qword_141B60C38 )
        goto LABEL_8;
    }
    if ( v6 == qword_141B60C38 )
      v7 = nullptr;
    else
      v7 = *(__int64 **)(v6 + 8);
  }
LABEL_8:
  v8 = &qword_141B5A4A0;
  if ( v7 == nullptr )
    v7 = &qword_141B5A4A0;
  v9 = v25;
  if ( v25 == v26 )
    goto LABEL_13;
  while ( *(_DWORD *)v9 != 1685353593 )
  {
    v9 += 16;
    if ( v9 == v26 )
      goto LABEL_13;
  }
  if ( v9 == v26 || (v12 = *(__int64 **)(v9 + 8)) == nullptr )
  {
LABEL_13:
    sub_140835A40(&v25, 1685353593, v7);
  }
  else if ( v12 != v7 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v12 + 16LL))(*v12, v12);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v7 + 24LL))(*v7, v7, v12);
  }
  v10 = qword_141B60C30;
  v11 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v10 != 1685417577 )
    {
      v10 += 16;
      if ( v10 == qword_141B60C38 )
        goto LABEL_25;
    }
    if ( v10 == qword_141B60C38 )
      v11 = nullptr;
    else
      v11 = *(__int64 **)(v10 + 8);
  }
LABEL_25:
  if ( v11 == nullptr )
    v11 = &qword_141B5A4A0;
  v13 = v25;
  v14 = v26;
  if ( v25 == v26 )
    goto LABEL_30;
  while ( *(_DWORD *)v13 != 1685417577 )
  {
    v13 += 16;
    if ( v13 == v26 )
      goto LABEL_30;
  }
  if ( v13 == v26 || (v20 = *(__int64 **)(v13 + 8)) == nullptr )
  {
LABEL_30:
    sub_140835A40(&v25, 1685417577, v11);
  }
  else if ( v20 != v11 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v20 + 16LL))(*v20, v20);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v11 + 24LL))(*v11, v11, v20);
  }
  v15 = sub_14083D4F0(v14);
  v28 = a2;
  v27 = v15 + 56;
  sub_140835380(&v25, 1886549113, &v27);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
  v16 = v25;
  if ( v25 == v26 )
    goto LABEL_34;
  while ( *(_DWORD *)v16 != 1853322860 )
  {
    v16 += 16;
    if ( v16 == v26 )
      goto LABEL_34;
  }
  if ( v16 == v26 || (v21 = *(_QWORD **)(v16 + 8)) == nullptr )
  {
LABEL_34:
    sub_140835A40(&v25, 1853322860, a3);
  }
  else if ( v21 != a3 )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v21 + 16LL))(*v21, v21);
    (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 24LL))(*a3, a3, v21);
  }
  v17 = qword_141B60C30;
  v18 = 0;
  v19 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v17 != 1986359923 )
    {
      v17 += 16;
      if ( v17 == qword_141B60C38 )
        goto LABEL_50;
    }
    if ( v17 == qword_141B60C38 )
      v19 = nullptr;
    else
      v19 = *(__int64 **)(v17 + 8);
  }
LABEL_50:
  if ( v19 != nullptr )
    v8 = v19;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v8 + 8LL))(*v8, v8) != 0 )
    v18 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v8 + 64LL))(*v8, v8);
  v23 = sub_14083D4F0(v22);
  v28 = v18;
  v27 = v23 + 40;
  sub_140835380(&v25, 1986359923, &v27);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
  sub_14083DDA0(&v27, &v25);
  sub_14083B5F0(a1 + 1816, &v27);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
  return sub_140833970(&v25);
}
