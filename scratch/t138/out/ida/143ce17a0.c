char __fastcall sub_143CE17A0(__int64 a1)
{
  _QWORD *v2; // r15
  _QWORD *v3; // r14
  _QWORD *v4; // rbx
  _QWORD *v5; // rdi
  __int64 v6; // rdi
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  _QWORD *v11; // rdi
  char result; // al
  __int64 v13; // rbx
  __int64 v14; // rcx
  __int64 v15; // rdi
  signed __int32 v16; // et0

  v2 = *(_QWORD **)(a1 + 128);
  v3 = (_QWORD *)*v2;
  v4 = (_QWORD *)v2[1];
  if ( (_QWORD *)*v2 != v4 )
  {
    v5 = (_QWORD *)*v2;
    do
    {
      if ( *v5 != 0 )
        (**(void (__fastcall ***)(_QWORD, __int64))*v5)(a1: *v5, a2: 1);
      ++v5;
    }
    while ( v5 != v4 );
    v6 = v2[1] - (_QWORD)v4;
    sub_141758A00(a1: v3, a2: v4, a3: v6);
    v2[1] = (char *)v3 + v6;
  }
  v7 = *(_QWORD *)(a1 + 96);
  if ( v7 != *(_QWORD *)(a1 + 104) )
    *(_QWORD *)(a1 + 104) = v7;
  v8 = *(_QWORD *)(a1 + 136);
  if ( v8 != *(_QWORD *)(a1 + 144) )
    *(_QWORD *)(a1 + 144) = v8;
  *(_BYTE *)(a1 + 160) = 0;
  v9 = *(_QWORD *)(a1 + 56);
  if ( v9 != *(_QWORD *)(a1 + 64) )
    *(_QWORD *)(a1 + 64) = v9;
  v10 = *(_QWORD *)(a1 + 8);
  if ( v10 != *(_QWORD *)(a1 + 16) )
    *(_QWORD *)(a1 + 16) = v10;
  v11 = *(_QWORD **)(a1 + 32);
  result = sub_1400D93A0(a1: a1 + 32, a2: a1 + 32, a3: v11[1]);
  v11[1] = v11;
  *v11 = v11;
  v11[2] = v11;
  *(_QWORD *)(a1 + 40) = 0;
  v13 = *(_QWORD *)(a1 + 48);
  if ( v13 != 0 )
  {
    sub_14083B0A0(a1: *(_QWORD *)(a1 + 48));
    v15 = sub_14082ABE0(a1: v14);
    MEMORY[0x1419475D8](a1: v15 + 32, a2: v13);
    if ( *(_BYTE *)(v15 + 72) != 0 )
    {
      v16 = _InterlockedDecrement((volatile signed __int32 *)(v15 + 64));
      result = v16 != 0;
      if ( v16 != 0 )
        goto LABEL_22;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v15 + 97) != 0 )
      result = sub_1412D33C0(a1: v15);
  }
LABEL_22:
  *(_QWORD *)(a1 + 48) = 0;
  *(_DWORD *)(a1 + 80) = 0;
  *(_WORD *)(a1 + 89) = 0;
  return result;
}
