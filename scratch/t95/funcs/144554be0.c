__int64 __fastcall sub_144554BE0(__int64 a1)
{
  __int64 *v1; // rdx
  __int64 v2; // rax
  __int64 v3; // rdx
  _QWORD *v4; // r8
  __int64 v5; // rdx
  __int64 v6; // rdx
  __int64 v7; // rbx
  __int64 v8; // rdi
  __int64 v9; // rsi
  __int64 *v10; // rdi
  _QWORD *v11; // rax
  __int64 v12; // rsi
  _QWORD *v13; // rbx
  __int64 v14; // rdi
  __int64 v15; // rcx
  __int64 v16; // rsi
  __int64 result; // rax
  __int64 v18; // rdi
  __int64 i; // rbx

  v1 = *(__int64 **)(qword_141B5FDB0 + 128);
  v2 = *v1;
  v3 = v1[1];
  while ( v2 != v3 )
  {
    if ( *(_QWORD *)(*(_QWORD *)v2 + 40LL) == a1 )
      *(_QWORD *)(*(_QWORD *)v2 + 40LL) = 0;
    v2 += 8;
  }
  v4 = (_QWORD *)qword_141B5FE00;
  v5 = *(_QWORD *)(*(_QWORD *)(qword_141B5FE00 + 128) + 8LL) - **(_QWORD **)(qword_141B5FE00 + 128);
  if ( v5 != 0 )
  {
    v6 = v5 >> 3;
    v7 = 0;
    while ( (int)v7 >= 0 )
    {
      if ( (_BYTE)word_141B60320 != 0 || (v9 = v4[12], (v4[13] - v9) >> 3 <= (unsigned __int64)(unsigned int)v7) )
      {
        v11 = (_QWORD *)v4[16];
        v12 = v11[1] - *v11;
        if ( v12 == 0 || v12 >> 3 <= (unsigned __int64)(unsigned int)v7 )
          break;
        v10 = (__int64 *)(*v11 + 8LL * (unsigned int)v7);
      }
      else
      {
        v10 = (__int64 *)(v9 + 8LL * (unsigned int)v7);
      }
      v8 = *v10;
      if ( *(_QWORD *)(v8 + 104) == a1 )
LABEL_18:
        *(_QWORD *)(v8 + 104) = 0;
LABEL_9:
      if ( v6 == ++v7 )
        goto LABEL_19;
    }
    v8 = 0;
    if ( MEMORY[0x68] == a1 )
      goto LABEL_18;
    goto LABEL_9;
  }
LABEL_19:
  v13 = *(_QWORD **)(qword_141B5FE48 + 128);
  v14 = *(_QWORD *)(*v13 + 8LL * *(int *)(a1 + 8));
  if ( v14 != 0 )
  {
    v15 = *(_QWORD *)(v14 + 24);
    if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 - 4)) == 0 )
      sub_1412EC9A0(v15 - 4);
    sub_140FAEBD0(v14);
  }
  sub_141758A00();
  v13[1] -= 8LL;
  v16 = qword_141B5FE48;
  result = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5FE48 + 48LL))(qword_141B5FE48);
  if ( result != 0 )
  {
    v18 = result;
    for ( i = 0; i != v18; ++i )
    {
      result = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v16 + 16LL))(v16, (unsigned int)i);
      *(_DWORD *)(result + 8) = i;
    }
  }
  return result;
}
