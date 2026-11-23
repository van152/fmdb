__int64 __fastcall sub_143E95F50(__int64 a1, _QWORD *a2)
{
  _QWORD *v2; // r13
  _QWORD *v4; // rax
  _QWORD *v5; // rax
  __int64 v6; // rax
  __int64 v7; // rcx
  unsigned __int64 i; // rdi
  __int64 v9; // rsi
  char v10; // bl
  _BYTE v12[8]; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v13[10]; // [rsp+30h] [rbp-10h] BYREF

  v13[2] = -2;
  if ( a2 == nullptr )
    return 0;
  v2 = a2;
  if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) != 3 )
  {
    v5 = v2;
LABEL_7:
    v2 = v5;
    goto LABEL_8;
  }
  v4 = (_QWORD *)v2[3];
  if ( v4 != (_QWORD *)v2[4] )
  {
    v5 = (_QWORD *)*v4;
    if ( v5 != nullptr )
      goto LABEL_7;
  }
LABEL_8:
  v6 = *(_QWORD *)(a1 + 432);
  v7 = *(_QWORD *)(a1 + 440);
  if ( v7 != v6 )
  {
    for ( i = 0; i < (v7 - v6) >> 3; ++i )
    {
      v9 = *(_QWORD *)(v6 + 8 * i);
      if ( v9 != 0 )
      {
        (*(void (__fastcall **)(_QWORD *, _BYTE *))(*v2 + 144LL))(v2, v12);
        v10 = sub_140FEB670(v9, v12);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v13[0] + 16LL))(v13[0], v13);
        if ( v10 != 0 )
          return v9;
        v6 = *(_QWORD *)(a1 + 432);
        v7 = *(_QWORD *)(a1 + 440);
      }
    }
  }
  return 0;
}
