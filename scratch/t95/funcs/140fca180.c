// THUNK ALIAS -> sub_143E01F10 (jmp:0x140fca180->0x143e01f10)
__int64 __fastcall sub_143E01F10(__int64 a1, char a2, __int64 a3)
{
  unsigned int v3; // edi
  __int64 v5; // rdx
  __int64 v7; // rax
  unsigned int v8; // eax
  int v9; // ecx
  __int64 v10; // rbx
  __int64 v11; // rbx
  unsigned __int8 v12; // al
  int v13; // ecx

  v5 = *(unsigned __int8 *)(a1 + 40);
  if ( (_BYTE)v5 == 0 )
    return 0;
  if ( a2 != 0 )
  {
    v7 = *(_QWORD *)(a1 + 80);
    if ( v7 != 0 && *(_QWORD *)(v7 + 96) != 0 )
    {
      v8 = *(unsigned __int8 *)(v7 + 244);
      if ( v8 <= 0xE )
      {
        LOBYTE(v3) = 1;
        v9 = 16387;
        if ( _bittest(&v9, v8) )
          return v3;
      }
    }
    v10 = 368;
    if ( *(_BYTE *)(a1 + 47) == 0 )
      v10 = 216;
    v11 = *(_QWORD *)(*(_QWORD *)(a1 + 48) + v10);
    if ( v11 != 0 )
    {
      LOBYTE(a3) = 1;
      if ( (unsigned __int8)sub_140CC6A10(v11, v5, a3, 0) != 0 )
      {
        v3 = 0;
        if ( (unsigned __int8)sub_140CC6A10(v11, *(unsigned __int8 *)(a1 + 40), 0, 0) == 0 )
          return v3;
      }
    }
  }
  v12 = *(_BYTE *)(a1 + 40);
  if ( v12 <= 0x1Eu )
  {
    v13 = 1073995784;
    LOBYTE(v3) = _bittest(&v13, v12);
    return v3;
  }
  return 0;
}
