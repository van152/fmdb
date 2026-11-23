_WORD *__fastcall sub_143C26860(__int64 a1, _WORD *a2, int a3)
{
  __int64 **v3; // rax
  int v5; // esi
  __int64 v6; // rdx
  __int64 v7; // r8
  __int64 **v8; // rcx
  __int64 *v9; // rdi
  unsigned int v10; // ebx

  LODWORD(v3) = a3;
  v5 = 1049072;
  while ( 1 )
  {
    v6 = a1;
    if ( ((unsigned __int8)v3 & 1) == 0 )
      break;
    v7 = (unsigned int)v3;
    v3 = *(__int64 ***)(a1 + 280);
    v8 = *(__int64 ***)(a1 + 288);
    if ( v3 == v8 )
    {
LABEL_11:
      LOBYTE(v7) = 1;
      goto LABEL_12;
    }
    while ( 1 )
    {
      v9 = *v3;
      if ( (*v3)[1] == v6 )
      {
        v10 = *((unsigned __int8 *)v9 + 48);
        if ( v10 <= 0x14 )
        {
          if ( _bittest(&v5, v10) )
            break;
        }
      }
      if ( ++v3 == v8 )
        goto LABEL_11;
    }
    a1 = *v9;
    LOBYTE(v3) = 1;
    if ( *v9 == 0 )
      goto LABEL_12;
  }
  v7 = 0;
LABEL_12:
  *a2 = 0;
  LOBYTE(v7) = v7 & 1;
  sub_141525ED0(a2, v6, v7);
  return a2;
}
